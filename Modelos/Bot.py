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
        ('system', 'Atendende de uma dentista '),
        ('system', 'reposta unica nome , maicon sem letra maiuscula'),
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
