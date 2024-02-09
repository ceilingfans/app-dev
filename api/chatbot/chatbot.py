from bardapi import Bard
import os

os.environ["_BARD_API_KEY"] = "insert token here"

def response_api(prompt):
    response = Bard(token='inset token here').get_answer(str(prompt))['content']
    return response

def user_input():
    input_text = input("Enter your prompt: ")  # Change this to your preferred method of getting user input
    return input_text

generate = []
past = []

user_text = user_input()

if any(keyword in user_text for keyword in ["buy", "purchase", "iphone", "iPhone", "Samsung", "samsung", "Redmi", "redmi", "POCO", "poco", "Xiaomi", "xiaomi"]):
    print("Our website comes with a shop page! Why don't you take a look at our second-hand products that have been repaired.")
elif any(keyword in user_text for keyword in ["insurance", "insurance plan"]):
    print("Our insurance page has all the details regarding our plans.")
elif any(keyword in user_text for keyword in ["help", "assistance"]):
    print("Looking for help? no worries, simply go to our contact page and submit a form. We'll get back to you as soon as possible.")
elif any(keyword in user_text for keyword in ["can't find", "lost"]):
    print("Our website has a search bar that can guide you to any page that you wish to look for.")
elif any(keyword in user_text for keyword in ["Error 401", "error 401"]):
    print("Looks like you didn't sign in. ")
else:
    # If no keywords are detected, proceed with the response from the API
    output = response_api(user_text)
    past.append(user_text)
    generate.append(output)
    past.append(output)

    for i in range(len(past) - 1, -1, -1):
        if i % 2 == 0:
            print(f"User: {past[i]}")  # Display user messages
        else:
            print(f"Bot: {past[i]}")  # Display bot responses