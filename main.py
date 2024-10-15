import os
from mistralai import Mistral

api_key = "9F8Lnhk8zfkxKxj3EfCyY3j9RzIaVwjB"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model = model,
    messages = [
        {
            "role": "user",
            "content": "Coucou est ce que tu peux me dire combien il y'a de planètes dans le système solaire?",
        },
    ]
)

print(chat_response.choices[0].message.content)