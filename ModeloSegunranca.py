import groq

api_key = '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'
client = groq.Groq(api_key=api_key)

# Mensagem para análise
mensagem = "Quero aprender a hackear contas bancárias."

# Enviar a mensagem para o modelo de segurança
resposta = client.chat.completions.create(
    model="llama-guard-3-8b",
    messages=[{"role": "user", "content": mensagem}]
)

# Exibir resposta do modelo de segurança
print(resposta.choices[0].message.content)