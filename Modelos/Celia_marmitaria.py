import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import telebot


# Configuração do cardápio
cardapio = [
    "Célia Marmitaria",
    "Cardápio do dia - Quarta-feira",
    "Pratos:",
    "- Arroz",
    "- Feijão",
    "- Estrogonofe de carne",
    "- Frango a Parmegiana",
    "- Bisteca de porco",
    "- Calabresa acebolada",
    "- Frango milanesa",
    "- Frango grelhado",
    "- Batata palha ou fritas",
    "",
    "Tamanhos:",
    "- Mini: 18",
    "- Média: 20",
    "- Grande: 24",
    "",
    "Refrigerantes:",
    "- Coca Cola 2 litros: 12,00",
    "- Refriko 2 litros: 8,00",
    "- Coca 600ml: 7,00",
    "- Lata: 5,00"
]
cardapio_str = "\n".join(cardapio)  # Transforma a lista de cardápio em uma string única

# Configuração da API Groq
api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

# Inicialização do modelo de chatbot
chat = ChatGroq(model='llama-3.3-70b-versatile')

def resposta_bot(mensagens):
    # Mensagens iniciais do chatbot
    mensagens_modelo = [
        ('system', 'Assistente de atendimento Marmitaria Celia'),
        ('system', f'Responda com base nos dados:\n{cardapio_str}')
    ]

    # Adiciona mensagens do usuário
    mensagens_modelo += mensagens
    # Cria o template sem metadados adicionais
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({}).content

# Configuração do bot Telegram
TELEGRAM_BOT_TOKEN = '7352539677:AAFuyYDwKm1jNjBT9KZnvT51jBGawQsmI-Y'  # Substitua pelo token do seu bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Dicionário para armazenar as conversas dos usuários
conversas_usuarios = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bem-vindo ao AsimoBot! Envie suas perguntas ou digite 'x' para encerrar.")

@bot.message_handler(func=lambda msg: True)
def responder(message):
    chat_id = message.chat.id
    pergunta = message.text.strip()

    # Inicializa a conversa para novos usuários
    if chat_id not in conversas_usuarios:
        conversas_usuarios[chat_id] = []

    # Checa se o usuário quer encerrar a conversa
    if pergunta.lower() == 'x':
        bot.send_message(chat_id, "Muito obrigado por usar o AsimoBot!")
        conversas_usuarios[chat_id] = []  # Reseta a conversa para este usuário
        return

    # Adiciona a pergunta do usuário e gera resposta
    conversas_usuarios[chat_id].append(('user', pergunta))
    resposta = resposta_bot(conversas_usuarios[chat_id])
    conversas_usuarios[chat_id].append(('assistant', resposta))

    # Envia a resposta para o usuário
    bot.send_message(chat_id, f'Bot: {resposta}')

# Inicia o bot
print("AsimoBot está ativo no Telegram.")
bot.polling()
