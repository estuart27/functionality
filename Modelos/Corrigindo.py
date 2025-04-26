import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

# chat = ChatGroq(model='llama-3.3-70b-versatile')
chat = ChatGroq(model='deepseek-r1-distill-llama-70b')

def resposta_bot(mensagens):
    mensagens_modelo = [
        ('system', 'assistente de endereço , corrija o endereço e mande o endereço corrigido'),
        ('system', 'Mande o endereço pronto para ser pesquisado no google mapa'),
        ('system', 'Exemplo:R. Francisco Arias, 671 - Conj. Semiramis Barros Braga, Londrina - PR, 86088-050'),
        ('system', 'Seja direto , mande somente o endereço corrigido'),

    ]

    mensagens_modelo += mensagens  # Adiciona as mensagens do usuário

    # Cria o template sem metadados adicionais
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    
    # Chama o modelo e retorna a resposta
    return chain.invoke({}).content

print('Bem-vindo')

mensagens = []
while True:
    pergunta = input('Usuário: ')
    if pergunta.lower() == 'x':
        break
    
    mensagens.append(('user', pergunta))  # Armazena a pergunta do usuário
    resposta = resposta_bot(mensagens)     # Obtém a resposta do bot
    mensagens.append(('assistant', resposta))  # Armazena a resposta do bot
    print(f'Bot: {resposta}')
    
    if resposta.lower() == 'vai estuart':  # Verifica se a resposta é 'VAI ESTUART'
        print('Safado')
print('Muito obrigado ')