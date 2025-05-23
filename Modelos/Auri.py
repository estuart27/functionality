import os
from groq import Groq

client = Groq(api_key="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")
filename = "som/MisterCuca.mp3"

with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
      file=(filename, file.read()),
      model="whisper-large-v3-turbo",
      response_format="verbose_json",
    )
    print(transcription.text)