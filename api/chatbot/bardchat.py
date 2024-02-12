from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
os.environ['OPENAI_API_KEY']


def bardchat(message):
    completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a technical assistant, skilled in explaining phones and phone insurance."},
    {"role": "user", "content": message}
  ]
)

    response = completion.choices[0].message.content
    
    data = str(response).replace("*", "")
    return data

