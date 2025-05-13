import google.generativeai as genai

# Configurar chave da API
genai.configure(api_key="AIzaSyCcKY-JfSfufUhAAkkiZ57ZAtPkG8e9wxs")  # Substitua pela sua chave

# Inicializar o modelo (use 'gemini-1.5-flash' para respostas rápidas ou 'gemini-1.5-pro' para mais qualidade)
# model = genai.GenerativeModel('gemini-1.5-pro')
model = genai.GenerativeModel('gemini-1.5-flash')


def pesquisar(pergunta):
    try:
        response = model.generate_content(pergunta)
        print("\n🔍 Resposta:\n")
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
