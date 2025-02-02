from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# Carregar modelo CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Carregar imagem
image = Image.open("exemplo3.jpg")

# Possíveis descrições
texts = ["Um gato", "Um cachorro", "Um carro", "Uma árvore", "Uma casa",'hidrante','Lobo']

# Preparar entrada
inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)

# Obter similaridade entre imagem e texto
outputs = model(**inputs)
logits_per_image = outputs.logits_per_image
probs = logits_per_image.softmax(dim=1)

# Mostrar resultado
print("Provável descrição:", texts[probs.argmax()])
