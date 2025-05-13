from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Carrega o modelo pré-treinado (você pode trocar o modelo por outro da Hugging Face)
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Histórico da conversa
chat_history_ids = None

print("Chatbot IA iniciado. Digite 'sair' para encerrar.")

while True:
    user_input = input("Você: ")
    if user_input.lower() == "sair":
        break

    # Tokeniza a entrada do usuário
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Concatena com o histórico (se houver)
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    # Gera a resposta
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Decodifica e imprime
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    print("Bot:", bot_response)


# ✅ O que esse código faz?
# Usa o modelo DialoGPT-medium da Microsoft (ótimo para bate-papo).

# Mantém o histórico da conversa para que o modelo entenda o contexto.

# Responde a cada mensagem do usuário com base no que foi dito anteriormente.

# 🔁 Quer algo mais avançado?
# Você pode:

# Trocar o modelo (ex: usar meta-llama, google/gemma, OpenChat etc.)

# Integrar com interfaces como Gradio para ter um chatbot com interface gráfica na web.

# Executar via Spaces no Hugging Face ou colocar online com Flask ou FastAPI.

# Se quiser, posso gerar um exemplo com interface visual ou te ajudar a publicar isso na web. Deseja?