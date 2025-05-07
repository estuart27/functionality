import os
from browser_use import Agent
import asyncio
from langchain_groq import ChatGroq  # Certifique-se de que esse pacote está instalado

# Configurar a chave de API da Groq
api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

# Inicializar o modelo LLaMA-3.3 70B via Groq
llm = ChatGroq(model='llama-3.3-70b-versatile')

async def main():
    agent = Agent(
        task="Entre em www.silvestrecode.shop, e busque por 'Bahia x Corinthians'",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
