from pydantic import BaseModel
from openai import OpenAI
import json
import os

"""
What is chain of thought?

Chain of thought
You can ask the model to output an answer in a structured, 
step-by-step way, to guide the user through the solution.

"""

class Step(BaseModel):
    """
    @details This class stores an explanation of a step and its corresponding output 
    in a step-by-step solution to a mathematical problem.

    @var explanation A detailed explanation of the step.
    @var output The result/output of the step.
    """
    explanation: str
    output: str

#
class MathReasoning(BaseModel):
    """
    @brief Represents the reasoning process for solving a math problem.

    @details This class holds a list of solution steps and the final computed answer.

    @var steps A list of Step objects that break down the solution.
    @var final_answer The final answer after completing all the steps.
    """
    steps: list[Step]
    final_answer: str


class CChatGPT:
    """
    @brief Wrapper for OpenAI's ChatGPT API.

    @param api_key OpenAI API key (optional).
    @param model GPT model (default: "gpt-3.5-turbo").

    @throws ValueError if API key is missing.

    @var api_key Authentication key.
    @var client OpenAI client instance.
    @var model Selected GPT model.
    """
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        """
        @brief Initializes CChatGPT.

        @param api_key API key (optional).
        @param model GPT model.

        @throws ValueError if API key is not provided.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def send_message(self, msg):
        """
        @brief Sends a message to ChatGPT.

        @param msg User input.

        @return GPT response or error message.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": msg}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e}"

# Usage example
if __name__ == "__main__":

    #test for CHATGPT CLASS
    # chat_gpt = CChatGPT()
    # response = chat_gpt.send_message("Write a haiku about recursion in programming.")
    # print(response)


    #test for MATHREASONING CLASS. a class used to demonstrate chain of thought. Output is in math_solution.json
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is required.")

    client = OpenAI(api_key=api_key)
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful math tutor. Guide the user step by step."},
                {"role": "user", "content": "how can I solve 8x + 7 = -23"}
            ],
            response_format=MathReasoning,
        )

        math_reasoning = completion.choices[0].message.parsed

        # Convert the response to a dictionary and save it to a JSON file
        with open("math_solution.json", "w") as json_file:
            json.dump(math_reasoning.dict(), json_file, indent=4)

        print("Response saved to math_solution.json")

    except Exception as e:
        print(f"Error: {e}")