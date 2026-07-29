from google import genai
from dotenv import load_dotenv
import os
from utils import apps

load_dotenv("config/.env")

key=os.getenv('gemini_key')

client=genai.Client(api_key=key)
tools=[apps.open_app,apps.close_app]

while True:
    prompt=input("You: ")
    interaction=client.models.generate_content(model='gemini-flash-latest',
                                       contents=prompt,config={
                                           "tools": tools
                                       })
    output=interaction.text
    print(f'Gemini: {output}')