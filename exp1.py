from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="",
)

history = "Hello"

for i in range(10):
    scammer = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[
            {
                "role": "user",
                "content": "You are now in an experiment where you must behave like a scam caller, The context is india so you must talk in hinglish. You will receive an input from the caller and based on that you will carry the conversation by being the scam caller.Don't give any annotation or translation in response just simple hinglish answer short and simple like a caller would.Carry only one sentence at a time,Conversation history so far:"
                + history,
            }
        ],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True,
    )
    print("Scammer:")

    for chunk in scammer:
        if chunk.choices[0].delta.content is not None:
            history += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    history = "Scammer:" + history

    caller = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[
            {
                "role": "user",
                "content": "You are in an experiment and you are a caller who is receiving a call that can or cannot be fruad you don't know jsut carry the conversation.Don't give any annotation or translation in response just simple hinglish answer short and simple like a caller would Speak in hinglish. Carry only one sentence at a time,Conversation history so far:"
                + history,
            }
        ],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True,
    )
    print()
    print("Caller:")
    for chunk in caller:
        if chunk.choices[0].delta.content is not None:
            history += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    history = "Caller:" + history
    print()


file = open("convo.txt", "w+")
file.write(history)
file.close()
