import groq

api_key = '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'
client = groq.Groq(api_key=api_key)

# Caminho do arquivo de áudio (substitua pelo seu arquivo)
audio_path = "som/MisterCucanao.mp3"

# Abrir e enviar o arquivo de áudio para transcrição
with open(audio_path, "rb") as audio_file:
    response = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",  # Escolha entre whisper-large-v3 ou whisper-large-v3-turbo
        file=audio_file,
        language="pt",  # Define o idioma como português
        response_format="text"  # Retorna o texto diretamente
    )

# Exibir o texto transcrito
print("Texto transcrito:")
print(response)
