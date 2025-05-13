import google.generativeai as genai
from PIL import Image
import io

# Configure sua chave da API
genai.configure(api_key="AIzaSyCcKY-JfSfufUhAAkkiZ57ZAtPkG8e9wxs")

# Use o modelo multimodal
# model = genai.GenerativeModel('gemini-1.5-pro')
model = genai.GenerativeModel('gemini-1.5-flash')

def pesquisar_com_imagem(pergunta, caminho_imagem):
    try:
        # Carregar a imagem com PIL
        imagem = Image.open(caminho_imagem)

        # Converter imagem PIL para bytes
        img_byte_arr = io.BytesIO()
        imagem.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()

        # Enviar imagem + pergunta como conteúdo multimodal
        response = model.generate_content(
            [
                {"mime_type": "image/jpeg", "data": img_bytes},
                pergunta
            ]
        )

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
        # caminho = input("Caminho da imagem (ou pressione Enter para pular): ")
        caminho = 'img/exemplo.jpg'
        if caminho.strip():
            pesquisar_com_imagem(pergunta, caminho)
        else:
            # Modo texto puro
            try:
                response = model.generate_content(pergunta)
                print("\n🔍 Resposta:\n")
                print(response.text)
            except Exception as e:
                print("Erro:", e)
