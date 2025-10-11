from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["Gem_api1"])


def receiver(history: str) -> str:
    context = f"""You are a person on a call and you are the receiver and you have to respond to a caller in hinglish the call history
                till now has been {history} give responses in json the response should look like this "message":"response here" if you don't know the name of the other person ask invent the necessary details the response should not contain any unorganic substance everything should feel organic"""
    resp = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=context
    )
    return resp.text[24:-7]
