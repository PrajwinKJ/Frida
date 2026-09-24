from openai import OpenAI
models={}

def create_client(key):
    client = OpenAI(
    api_key=key,
    base_url="https://api.groq.com/openai/v1",
)

def provider(provider):
    def name(func):
        models[func.__name__]={
            'provider':provider,
            'object':func
        }
        return func
    return name

@provider("groq")
class openai_20b:
    def __init__(self,api_key):
        self.key=api_key
        self.client = OpenAI(
        api_key=self.key,
        base_url="https://api.groq.com/openai/v1",
        )

    def response(self,user):
        completion=self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": user,
                }
            ],
            reasoning_effort='low'
        )
        return completion.choices[0].message

@provider("nvidia")
class nemotron:
    def __init__(self,api_key):
        self.key=api_key
        self.client = OpenAI(
        api_key=self.key,
        base_url="https://api.groq.com/openai/v1",
        )

    def response(self,user):
        completion=self.client.chat.completions.create(
            model="nvidia/nemotron-20b",
            messages=[
                {
                    "role": "user",
                    "content": user,
                }
            ],
            reasoning_effort='low'
        )
        return completion.choices[0].message