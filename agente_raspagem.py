import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Carregar chave de API de .env
load_dotenv()
api_key = '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'# Configuração da API Key de forma segura
if not api_key:
    raise ValueError("A chave GROQ_API_KEY não foi definida.")
os.environ['GROQ_API_KEY'] = api_key

# Inicializar o modelo Groq
llm = ChatGroq(model='gemma2-9b-it')

from browser_use import Agent  # Supondo que exista e esteja correto

async def main():
    agent = Agent(
        task="Entre em www.silvestrecode.shop, e busque por 'Bahia x Corinthians'",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
