import google.generativeai as genai
import json

# Configurar chave da API
genai.configure(api_key="AIzaSyCcKY-JfSfufUhAAkkiZ57ZAtPkG8e9wxs")  # Substitua pela sua chave

# Inicializar o modelo (Flash = mais rápido, Pro = mais completo)
model = genai.GenerativeModel('gemini-1.5-flash')

def pesquisar(pergunta):
    try:
        # Adiciona instrução para retornar apenas JSON válido
        prompt = pergunta.strip() + "\n\nRetorne apenas um JSON válido sem explicações extras."

        response = model.generate_content(prompt)

        resposta = response.text.strip()

        # Tenta carregar como JSON
        dados = json.loads(resposta)

        # Salva em arquivo
        with open("resposta.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

        print("\n✅ JSON salvo como 'resposta.json' com sucesso.")
    except json.JSONDecodeError:
        print("\n⚠️ A resposta não está em um formato JSON válido:")
        print(response.text)
    except Exception as e:
        print("Erro:", e)

# Exemplo de uso:
if __name__ == "__main__":
    while True:
        pergunta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        if pergunta.lower() == "sair":
            break
        pesquisar(pergunta)


# # Inicializar o modelo (use 'gemini-1.5-flash' para respostas rápidas ou 'gemini-1.5-pro' para mais qualidade)
# # model = genai.GenerativeModel('gemini-1.5-pro')
# model = genai.GenerativeModel('gemini-1.5-flash')


# def pesquisar(pergunta):
#     try:
#         response = model.generate_content(pergunta)
#         print("\n🔍 Resposta:\n")
#         print(response.text)
#     except Exception as e:
#         print("Erro:", e)

# # Exemplo de uso:
# if __name__ == "__main__":
#     while True:
#         pergunta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
#         if pergunta.lower() == "sair":
#             break
#         pesquisar(pergunta)
