import google.generativeai as genai
import json
import re

# Configure sua chave da API
genai.configure(api_key="AIzaSyCcKY-JfSfufUhAAkkiZ57ZAtPkG8e9wxs")

# Inicializar o modelo
model = genai.GenerativeModel('gemini-1.5-flash')

def extrair_json(texto):
    """Tenta extrair um JSON válido mesmo com texto antes ou depois."""
    try:
        # Tenta extrair o primeiro bloco entre { } ou [ ]
        match = re.search(r'(\{.*\}|\[.*\])', texto, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        else:
            return None
    except json.JSONDecodeError:
        return None

def pesquisar(pergunta):
    try:
        prompt = pergunta.strip() + "\n\nResponda apenas com um JSON válido."

        response = model.generate_content(prompt)
        resposta = response.text.strip()

        # Salva o texto bruto da resposta para debug
        with open("resposta_bruta.txt", "w", encoding="utf-8") as f:
            f.write(resposta)

        # Tenta extrair e salvar JSON
        dados = extrair_json(resposta)
        if dados:
            with open("resposta.json", "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            print("\n✅ JSON válido salvo em 'resposta.json'")
        else:
            print("\n❌ A resposta não está em formato JSON válido. Veja 'resposta_bruta.txt'.")
    except Exception as e:
        print("Erro inesperado:", e)

# Execução interativa
if __name__ == "__main__":
    while True:
        pergunta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        if pergunta.lower() == "sair":
            break
        pesquisar(pergunta)
