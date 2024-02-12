from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
os.environ['OPENAI_API_KEY']


def bardchat(message):
        if any(keyword in message for keyword in ["buy", "purchase", "iphone", "iPhone", "Samsung", "samsung", "Redmi", "redmi", "POCO", "poco", "Xiaomi", "xiaomi"]):
                data = "Our website comes with a shop page! Why don't you take a look at our second-hand products that have been repaired."
                return data
        elif any(keyword in message for keyword in ["insurance", "insurance plan"]):
                data = "Our insurance page has all the details regarding our plans."
                return data
        elif any(keyword in message for keyword in ["help", "assistance"]):
                data = "Looking for help? no worries, simply go to our contact page and submit a form. We'll get back to you as soon as possible."
                return data
        elif any(keyword in message for keyword in ["can't find", "lost"]):
                data = "Our website has a search bar that can guide you to any page that you wish to look for."
                return data
        elif any(keyword in message for keyword in ["Error 401", "error 401"]):
                data = "Please sign in."
                return data
        else:
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
