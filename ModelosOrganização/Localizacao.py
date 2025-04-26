import openrouteservice

API_KEY = "5b3ce3597851110001cf6248151bddc9bb50465286bed08b4efaa1b3"
client = openrouteservice.Client(key=API_KEY)

def calcular_distancia(origem, destino):
    """Calcula a distância entre dois pontos usando OpenRouteService."""
    # Inverter as coordenadas para [longitude, latitude]
    origem_invertido = [origem[1], origem[0]]
    destino_invertido = [destino[1], destino[0]]
    
    coordenadas = [origem_invertido, destino_invertido]
    
    try:
        resposta = client.directions(
            coordinates=coordenadas, 
            profile="driving-car", 
            format="geojson",
            radiuses=[55000, 55000]  # Raio de busca de 55km
        )
        distancia_km = resposta['features'][0]['properties']['segments'][0]['distance'] / 1000  # Converter para KM
        return distancia_km
    except Exception as e:
        print("Erro ao calcular distância:", e)
        return 0

def calcular_taxa_por_distancia(origem, destino):
    distancia = calcular_distancia(origem, destino)
    return distancia * 2.50  # R$2,50 por KM

# Exemplo de uso:
origem = (-23.31230857140604, -51.14313373855404)  # Londrina, Paraná (latitude, longitude)
destino = (-23.265074830680764, -51.146487577849754)  # Outro ponto em Londrina

print(f"Distância: {calcular_distancia(origem, destino):.2f} km")
print(f"Taxa de entrega: R$ {calcular_taxa_por_distancia(origem, destino):.2f}")
