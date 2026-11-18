'''
BLE link from this app to the Breathing Cube.

The cube advertises as "BreathingCube" only while it is on USB-C power.
This module keeps trying to find and connect to it in a background thread,
so the Tkinter UI never waits on Bluetooth.

App -> cube commands (see BreathingCubeSoftware/src/cube/drivers/cubeCommands.py):
    start_focus(seconds, task)  -> {"cmd":"focus","task_time":..,"task_name":..}
                                   cube saves the preset and (re)starts the
                                   session: breathing, alarm after `seconds`.
    stop()                      -> "stop": cube stops the timer and lights.

If the cube is not connected when a button is pressed, the latest command is
kept and sent once it connects. A pending focus is shortened by the time
already spent waiting (and dropped if that time has run out), so the cube
rings when the app's own timer does.

Tk is not thread-safe: read `status` / `connected` from the UI thread
(e.g. with root.after) instead of passing Tk callbacks in here.
'''

import asyncio
import json
import threading
import time

try:
    from bleak import BleakClient, BleakScanner
except ImportError:  # App still runs without the cube.
    BleakClient = BleakScanner = None

CUBE_NAME = "BreathingCube"
SERVICE_UUID = "6e2a0001-8f3b-4c1a-9b4e-2f1c0b5e7a10"
COMMAND_UUID = "6e2a0002-8f3b-4c1a-9b4e-2f1c0b5e7a10"
STATUS_UUID = "6e2a0003-8f3b-4c1a-9b4e-2f1c0b5e7a10"

SCAN_TIMEOUT_S = 5.0
RETRY_DELAY_S = 3.0
TASK_NAME_MAX = 40  # Keeps the JSON well under the cube's 128-byte buffer.


class CubeLink:
    def __init__(self, name=CUBE_NAME):
        self.name = name
        self.connected = False
        self.status = "Cube: Bluetooth unavailable (pip install bleak)" if BleakClient is None else "Cube: searching..."
        self.last_cube_status = None  # Latest JSON the cube notified.
        self._lock = threading.Lock()
        self._pending = None          # (kind, seconds, task, queued_at)
        self._loop = None
        self._wake = None
        self._stopping = False
        if BleakClient is None:
            print("CubeLink: bleak is not installed; cube sync disabled")
            return
        self._thread = threading.Thread(target=self._thread_main, name="CubeLink", daemon=True)
        self._thread.start()

    # ---------- Called from the UI thread ----------
    def start_focus(self, seconds, task=""):
        """Ask the cube to breathe and ring after `seconds`."""
        self._queue(("focus", int(seconds), (task or "").strip()[:TASK_NAME_MAX], time.monotonic()))

    def stop(self):
        """Ask the cube to stop its timer and lights."""
        self._queue(("stop", 0, "", time.monotonic()))

    def close(self):
        self._stopping = True
        self._poke()

    # ---------- Internals ----------
    def _queue(self, command):
        if BleakClient is None:
            return
        with self._lock:
            self._pending = command  # Only the latest command matters.
        self._poke()

    def _poke(self):
        if self._loop is not None and self._wake is not None:
            self._loop.call_soon_threadsafe(self._wake.set)

    def _thread_main(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._wake = asyncio.Event()
        try:
            self._loop.run_until_complete(self._run())
        except Exception as e:
            self.status = "Cube: link stopped (%s)" % e
            print("CubeLink stopped:", e)

    def _take_pending(self):
        with self._lock:
            command, self._pending = self._pending, None
        return command

    def _encode(self, command):
        """Bytes to send, or None if the command is stale."""
        kind, seconds, task, queued_at = command
        if kind == "stop":
            return b"stop"
        remaining = seconds - int(time.monotonic() - queued_at)
        if remaining <= 0:
            print("CubeLink: focus time ran out before the cube connected; not sent")
            return None
        body = {"cmd": "focus", "task_time": remaining}
        if task:
            body["task_name"] = task
        return json.dumps(body, separators=(",", ":")).encode("utf-8")

    def _on_status(self, _char, data):
        try:
            self.last_cube_status = json.loads(bytes(data).decode("utf-8"))
        except ValueError:
            return  # Notification cut at the MTU; a read would get it all.
        last = self.last_cube_status.get("last")
        if last:
            print("Cube:", last)

    def _on_disconnect(self, _client):
        self.connected = False
        self.status = "Cube: disconnected, searching..."
        self._poke()

    async def _run(self):
        while not self._stopping:
            self.status = "Cube: searching..."
            try:
                device = await BleakScanner.find_device_by_filter(
                    lambda d, adv: (d.name or "").startswith(self.name)
                    or SERVICE_UUID in [u.lower() for u in adv.service_uuids],
                    timeout=SCAN_TIMEOUT_S,
                )
            except Exception as e:  # Bluetooth off, no adapter, ...
                self.status = "Cube: Bluetooth error (%s)" % e
                await asyncio.sleep(RETRY_DELAY_S)
                continue
            if device is None:
                self.status = "Cube: not found (plug the cube into USB-C)"
                await asyncio.sleep(RETRY_DELAY_S)
                continue

            try:
                async with BleakClient(device, disconnected_callback=self._on_disconnect) as client:
                    self.connected = True
                    self.status = "Cube: connected"
                    print("CubeLink: connected to", device.address)
                    try:
                        await client.start_notify(STATUS_UUID, self._on_status)
                    except Exception as e:
                        print("CubeLink: status notifications unavailable:", e)
                    while client.is_connected and not self._stopping:
                        self._wake.clear()  # Before taking, so no poke is lost.
                        command = self._take_pending()
                        if command is not None:
                            data = self._encode(command)
                            if data is not None:
                                try:
                                    await client.write_gatt_char(COMMAND_UUID, data, response=True)
                                    print("CubeLink: sent", data.decode())
                                except Exception as e:
                                    print("CubeLink: send failed, will retry:", e)
                                    with self._lock:
                                        if self._pending is None:
                                            self._pending = command
                                    break
                            continue
                        try:
                            await asyncio.wait_for(self._wake.wait(), timeout=5.0)
                        except asyncio.TimeoutError:
                            pass
            except Exception as e:
                print("CubeLink: connection failed:", e)
            self.connected = False
            if not self._stopping:
                self.status = "Cube: disconnected, searching..."
                await asyncio.sleep(1.0)
