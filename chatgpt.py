import os
from dotenv import load_dotenv
from openai  import OpenAI
from core.oopschema import registry
import utils.appsoop
import json

features=[]
for i in registry.values():
    features.extend(i['schemas'])
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
            tools=features,
            tool_choice="auto"
        )
    chat=chat_completion.choices[0].message
    if chat.tool_calls:
        fn=chat.tool_calls[0].function
        arg=json.loads(fn.arguments)
        name=fn.name
        plugin,method=name.split('::',1)
        instance=registry[plugin]['instance']
        exe=getattr(instance,method)
        exe(**arg)
    else:
        print(f"Frida: {chat.content}")
