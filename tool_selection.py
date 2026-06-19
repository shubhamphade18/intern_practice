from dotenv import load_dotenv
from openai import OpenAI

import os
import json

# --------------------------
# Load Environment Variables
# --------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# --------------------------
# Tools
# --------------------------

def get_weather(city):
    return f"The weather in {city} is 28°C and Sunny."

def calculate(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return str(e)

# --------------------------
# Tool Definitions
# --------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather information for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of city"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# --------------------------
# User Query
# --------------------------

user_query = input("Ask: ")

messages = [
    {
        "role": "user",
        "content": user_query
    }
]

# --------------------------
# First LLM Call
# --------------------------

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

response_message = response.choices[0].message

# --------------------------
# Check Tool Calls
# --------------------------

if response_message.tool_calls:

    messages.append(response_message)

    for tool_call in response_message.tool_calls:

        function_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        # Execute Weather Tool
        if function_name == "get_weather":

            result = get_weather(
                arguments["city"]
            )

        # Execute Calculator Tool
        elif function_name == "calculate":

            result = calculate(
                arguments["expression"]
            )

        else:
            result = "Unknown tool"

        # Add tool result to conversation

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            }
        )

    # --------------------------
    # Second LLM Call
    # --------------------------

    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    print("\nAssistant:")
    print(final_response.choices[0].message.content)

else:

    print("\nAssistant:")
    print(response_message.content)