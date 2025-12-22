import os

import simpleaudio as sa
import soundfile as sf
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

# -----------------------------
# READ YOUR TEXT FILE
# -----------------------------
with open("Conv/conv_1.txt", "r") as f:
    context = f.read()

# -----------------------------
# DEVICE SETUP FOR MAC
# -----------------------------
device = "mps" if torch.backends.mps.is_available() else "cpu"

# -----------------------------
# LOAD MODEL + TOKENIZERS
# -----------------------------
model = ParlerTTSForConditionalGeneration.from_pretrained(
    "ai4bharat/indic-parler-tts"
).to(device)

tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-parler-tts")
description_tokenizer = AutoTokenizer.from_pretrained(
    model.config.text_encoder._name_or_path
)

# -----------------------------
# DESCRIPTION / VOICE STYLE
# (Change speaker here)
# -----------------------------
description = (
    "Divya's voice is natural, clear and expressive, slightly fast, "
    "with very clear audio recorded close to the microphone."
)

# Convert description & text to tokens
description_input = description_tokenizer(description, return_tensors="pt").to(device)
prompt_input = tokenizer(context, return_tensors="pt").to(device)

# -----------------------------
# GENERATE AUDIO
# -----------------------------
generation = model.generate(
    input_ids=description_input.input_ids,
    attention_mask=description_input.attention_mask,
    prompt_input_ids=prompt_input.input_ids,
    prompt_attention_mask=prompt_input.attention_mask,
)

audio_arr = generation.cpu().numpy().squeeze()

# -----------------------------
# SAVE AUDIO
# -----------------------------
filename = "output.wav"
sf.write(filename, audio_arr, model.config.sampling_rate)

# -----------------------------
# PLAY AUDIO
# -----------------------------
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
play_obj.wait_done()

print("Audio saved and played successfully!")
