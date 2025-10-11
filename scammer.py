from google import genai

from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.environ["Gem_api1"])


def caller(history: str, scam_context: str, responses: int) -> str:
    context = f"""You are a person on a call and you are the caller and you are actually a scammer and the context of your scam is {scam_context} the call history
                till now has been {history} Respond in hinglish if there is no conv history then start the conversation if there is then continue the conversation
                you only have {responses} left  give responses in json the response should look like this "message":"response here" if you don't know the name of the other person ask invent the necessary details the response should not contain any unorganic substance """
    resp = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=context
    )
    return resp.text[24:-7]
