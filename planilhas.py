import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

arquivo = "https://docs.google.com/spreadsheets/d/1LoVoIJurt8QSP9X7CLZqwQy8aPVRn5b6eKHTIQyPSFk/export?format=csv"
# "https://docs.google.com/spreadsheets/d/1LoVoIJurt8QSP9X7CLZqwQy8aPVRn5b6eKHTIQyPSFk/export?format=csv"

df = pd.read_csv(arquivo)

# Configura o pandas para mostrar todas as linhas e colunas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def carregar_documento_web():
    # Transforma o DataFrame em string no formato de tabela
    documento = df.to_string(index=False)

    # Define a chave da API Groq
    api_key = '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'
    os.environ['GROQ_API_KEY'] = api_key

    # Inicializa o modelo
    chat = ChatGroq(model='llama-3.3-70b-versatile',temperature=0.3)

    # Prompt template
    template = ChatPromptTemplate.from_messages([
        ('system', 'Você é uma analista de dados que vai responder perguntas sobre a seguinte planilha:\n{documentos_informados}'),
        ('user', '{input}')
    ])

    # Chama o modelo com a pergunta
    chain = template | chat
    resposta = chain.invoke({
        'documentos_informados': documento,
        'input': "o que essa planilha esta falando?, seja direto e objetivo"
    })

    return resposta.content

resposta = carregar_documento_web()
print(resposta)

#Lembrando  que esse codigo é somente para analises gerais , ele na é acertivo em sua contagem preciso de dados especificos 

