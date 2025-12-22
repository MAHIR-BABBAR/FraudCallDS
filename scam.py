import os
import time

from caller import receiver
from scammer import caller

os.makedirs("Conv", exist_ok=True)

with open("fraud_context.txt", "r", encoding="utf-8") as f:
    contexts = f.readlines()
    contexts = contexts[182:200]

for j, context in enumerate(contexts, start=1):
    history = ""
    print(f"Simulating conversation {j + 182}...")

    for i in range(5, 1, -1):
        scammer_resp = caller(history, context, i)
        history += f"caller: {scammer_resp}\n"
        time.sleep(10)
        receiver_resp = receiver(history)
        history += f"receiver: {receiver_resp}\n"
        time.sleep(10)

    with open(f"Conv/conv_{j + 182}.txt", "w", encoding="utf-8") as file:
        _ = file.write(history)

print("All conversations saved in 'Conv/' folder.")
