import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Saudação")
    root.geometry("200x100")
    
    label = tk.Label(root, text="Oi!", font=("Arial", 16))
    label.pack(pady=20)
    
    root.mainloop()    


api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.3-70b-versatile')

def resposta_bot(mensagens):
    mensagens_modelo = [
        ('system', 'Você é um vendedor de garfas de café e chá'),
        ('system', 'Na usa comunicação use a Técnica socrática , Técnica do contraste, Storytelling, e a Técnica de Vendas SPIN'),
        ('system', 'seja o mais objetivo possível para nao perder o foco e nem cansar o cliente'),
        ('system', 'reposta em portugues e respeitando o contexto'),
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

    if pergunta.lower() == 'maicon':
        main()
    
    mensagens.append(('user', pergunta))  # Armazena a pergunta do usuário
    resposta = resposta_bot(mensagens)     # Obtém a resposta do bot
    mensagens.append(('assistant', resposta))  # Armazena a resposta do bot
    print(f'Bot: {resposta}')
    
    if resposta.lower() == 'vai estuart':  # Verifica se a resposta é 'VAI ESTUART'
        print('Safado')
print('Muito obrigado ')

# pip install langchain-groq
# pip install langchain
