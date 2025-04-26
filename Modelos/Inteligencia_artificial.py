import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from groq import Groq


api_key = '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'
# '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'
os.environ['GROQ_API_KEY'] = api_key

# client = Groq(api_key=api_key)
# models = client.models.list()
# print(models)
# chat = ChatGroq(model='llama-3.3-70b-versatile')
# chat = ChatGroq(model='llama-3.1-8b-instant')
# chat = ChatGroq(model='mixtral-8x7b-32768')
# chat = ChatGroq(model='deepseek-r1-distill-llama-70b')
chat = ChatGroq(model='gemma2-9b-it')


def resposta_bot(mensagens):
    # Define uma mensagem inicial com o papel do assistente
    mensagens_modelo = [
        ('system', 'Vc vai ser um vendedor de imovel inteligente e atencioso.'),

    ]

    mensagens_modelo += mensagens
    # Cria o template sem metadados adicionais
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({}).content

print('Bem-vindo ao AsimoBot')

mensagens = []
while True:
    pergunta = input('Usuário: ')
    if pergunta.lower() == 'x':
        break
    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens)
    mensagens.append(('assistant', resposta))
    print(f'Bot: {resposta}')

print('Muito obrigado por usar o AsimoBot!')
