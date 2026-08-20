from openai import OpenAI
models={}

def create_client(key):
    client = OpenAI(
    api_key=key,
    base_url="https://api.groq.com/openai/v1",
)

def engines(provider):
    def name(func):
        models[func.__name__]={
            'provider':provider
        }
        return func
    return name

@engines("Groq")
class openai_20b:
    def __init__(self,api_key):
        self.key=api_key
        self.client = OpenAI(
        api_key=self.key,
        base_url="https://api.groq.com/openai/v1",
        )

    def response(self):
        completion=self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": 'hello',
                }
            ],
            reasoning_effort='low'
        )
        return completion.choices[0].message
print(models)
engine=openai_20b()
response=engine.response()
print(response.)