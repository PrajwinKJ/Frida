import os
from dotenv import load_dotenv
from openai  import OpenAI
from core.schema import tool_registry
import utils.apps
import json

tools=[tools['schema'] for tools in tool_registry.values()]


load_dotenv('config/.env')
client = OpenAI(
    api_key=os.getenv('groq_key'),
    base_url="https://api.groq.com/openai/v1",
)

while True:
    user=input("You: ")
    if user.lower()=='exit':
        break
    chat_completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": user
        }
    ],
    tools=tools,
    tool_choice="auto"
)

    chat=chat_completion.choices[0].message
    arguments=chat.tool_calls
    if arguments:
        fn=arguments[0].function.name
        arg=json.loads(arguments[0].function.arguments)
        reply=tool_registry[fn]['function'](arg['app_name'])
        if reply:
            print(f"{reply}")
    else:
        print(f"Jarvis: {chat.content}")