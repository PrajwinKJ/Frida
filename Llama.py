import os
from dotenv import load_dotenv
from core.schema import tool_registry
import utils.apps
load_dotenv('config/.env')
import json

from groq import Groq

tools=[tools['schema'] for tools in tool_registry.values()]

client = Groq(
    api_key=os.getenv('groq_key'),
)
while True:
    prompt=input("You: ")
    if not prompt.lower()=='exit':
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            tools=tools,
            tool_choice='auto'
        )

        chat=chat_completion.choices[0].message
        arguments=chat.tool_calls
        if arguments:
            fn=arguments[0].function.name
            arg=json.loads(arguments[0].function.arguments)
            print(arg)
            tool_registry[fn]['function'](arg['app_name'])
        else:
            print(f"Jarvis: {chat.content}")