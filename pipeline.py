import json
import os

print("Hello i am ")


from dotenv import load_dotenv

load_dotenv()

print("..")


import google.generativeai as genai

genai.configure(api_key=os.environ["Gem_api2"])
client = genai.GenerativeModel("gemini-2.5-flash-lite")


print("Hello i am running..")
os.makedirs("Conv3", exist_ok=True)

for i in range(1, 201):
    try:
        with open(f"Conv/conv_{i}.txt", "r") as f:
            print(f"Augumenting {i}")
            resp = client.generate_content(
                f"""You are given a conversation your job is to create another conversation like this but in a different context like this is a scam call
                so the topic of the scam must remain the same but content should be different the conversation is {f.read()} also return
                the conversation as provided in the text + Return the response in json + also invent the necessary details,
                The new conversation should be as large as the previous one"""
            )

            with open(f"Conv3/conv_{i}.txt", "w+") as f:
                resp = resp.text[7:-3]
                f.write(resp)
    except Exception as e:
        print("Error", e)
