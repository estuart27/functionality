import openrouteservice
from openrouteservice.geocode import pelias_search

API_KEY = "5b3ce3597851110001cf6248151bddc9bb50465286bed08b4efaa1b3"
client = openrouteservice.Client(key=API_KEY)

def obter_coordenadas(endereco):
    """Converte um endereço em texto para coordenadas [longitude, latitude]."""
    try:
        # Adicionando Brasil para melhorar a precisão da busca em endereços brasileiros
        endereco_completo = f"{endereco}, Brasil"
        resultados = pelias_search(client, endereco_completo)
        
        if resultados and len(resultados['features']) > 0:
            # Pega as coordenadas do primeiro resultado
            coord = resultados['features'][0]['geometry']['coordinates']
            # Retorna [longitude, latitude]
            return coord
        else:
            print(f"Não foi possível encontrar coordenadas para: {endereco}")
            return None
    except Exception as e:
        print(f"Erro ao converter endereço para coordenadas: {e}")
        return None

def calcular_distancia_por_endereco(endereco_origem, endereco_destino):
    """Calcula a distância entre dois endereços."""
    coord_origem = obter_coordenadas(endereco_origem)
    coord_destino = obter_coordenadas(endereco_destino)
    
    if not coord_origem or not coord_destino:
        return 0
    
    try:
        coordenadas = [coord_origem, coord_destino]
        resposta = client.directions(
            coordinates=coordenadas, 
            profile="driving-car", 
            format="geojson",
            radiuses=[55000, 55000]
        )
        distancia_km = resposta['features'][0]['properties']['segments'][0]['distance'] / 1000
        return distancia_km
    except Exception as e:
        print(f"Erro ao calcular distância: {e}")
        return 0

def calcular_taxa_por_endereco(endereco_origem, endereco_destino):
    """Calcula a taxa baseada na distância entre dois endereços."""
    distancia = calcular_distancia_por_endereco(endereco_origem, endereco_destino)
    return distancia * 2.50  # R$2,50 por KM

# Exemplo de uso com interface para o usuário
def main():
    print("=== Calculadora de Distância e Taxa de Entrega ===")
    
    endereco_origem = input("Digite o endereço de origem: ")
    endereco_destino = input("Digite o endereço de destino: ")
    
    # Obtém e mostra as coordenadas
    coord_origem = obter_coordenadas(endereco_origem)
    coord_destino = obter_coordenadas(endereco_destino)
    
    if coord_origem and coord_destino:
        print(f"\nCoordenadas de origem: [longitude: {coord_origem[0]}, latitude: {coord_origem[1]}]")
        print(f"Coordenadas de destino: [longitude: {coord_destino[0]}, latitude: {coord_destino[1]}]")
        
        distancia = calcular_distancia_por_endereco(endereco_origem, endereco_destino)
        taxa = calcular_taxa_por_endereco(endereco_origem, endereco_destino)
        
        print(f"\nDistância: {distancia:.2f} km")
        print(f"Taxa de entrega: R$ {taxa:.2f}")
    else:
        print("\nNão foi possível calcular a distância devido a um erro na obtenção das coordenadas.")

if __name__ == "__main__":
    main()