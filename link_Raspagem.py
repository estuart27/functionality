from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

# Carrega documentos da web
loader = WebBaseLoader("https://docs.google.com/spreadsheets/d/1Sm7k2kdpjYyfhGAhJYXlDheTTo4ifNuSbSneIvm-2Dc/edit?usp=sharing")
lista_documentos = loader.load()
# print(lista_documentos)

# Concatena conteúdo dos documentos
documento = ''
for doc in lista_documentos:
    documento = documento + doc.page_content
    print(doc.page_content)  # Verifique o conteúdo carregado
