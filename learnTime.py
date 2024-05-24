import time

# Get the current time as a struct_time object
current_time = time.localtime()

# Format the date and time into a more readable string
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)

# Print the formatted date and time
print("Current Date and Time:", formatted_time)
