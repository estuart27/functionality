from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os


def analizar_partida(URl):
    loader = WebBaseLoader(URl)
    lista_documentos = loader.load()

    # Concatena conteúdo dos documentos
    documento = ''
    for doc in lista_documentos:
        documento = documento + doc.page_content

    api_key = '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'
    os.environ['GROQ_API_KEY'] = api_key

    # Inicializa o ChatGroq
    chat = ChatGroq(model='deepseek-r1-distill-llama-70b')

    # Template de prompt para o assistente
    # template = ChatPromptTemplate.from_messages([
    #     ('system', 'você vai ser um apostador , que vai dar sugestões com base nós dados: {documentos_informados}'),
    #     ('user', '{input}')
    # ])

    template = ChatPromptTemplate.from_messages([
        ('system', 'Você é um especialista em apostas esportivas focado em fornecer análises detalhadas e previsões assertivas com base em dados estatísticos, contextuais e táticos.'),
        ('system', 'Use as informações detalhadas abaixo para realizar uma análise precisa e informar uma recomendação de aposta:{documentos_informados}'),
        ('system', """Dados e Critérios para Análise:

    1. **Forma Recente dos Times**:
    - Desempenho nos últimos 5 a 10 jogos, considerando vitórias, empates e derrotas, além de performance específica contra adversários de níveis similares.
    - Momento atual da equipe (sequências de vitórias, derrotas, padrão de gols marcados e sofridos).

    2. **Desempenho em Casa e Fora**:
    - Aproveitamento jogando em casa e como visitante, considerando histórico de confrontos e estilo de jogo (times que performam melhor em contra-ataques tendem a se sair bem fora de casa).
    - Impacto de apoio da torcida e histórico em estádios específicos.

    3. **Histórico de Confrontos Diretos (Head-to-Head)**:
    - Resultados recentes entre os times, incluindo margem de vitória e frequência de empates.
    - Análise de vantagens psicológicas ou estratégias que costumam funcionar contra o adversário.

    4. **Classificação na Tabela e Objetivos**:
    - Posição atual na tabela e contexto de motivação (disputa pelo título, classificação para torneios ou luta contra o rebaixamento).
    - Objetivos específicos de cada time, que podem influenciar o estilo de jogo e a agressividade na partida.

    5. **Estatísticas Ofensivas e Defensivas**:
    - Média de gols marcados e sofridos por jogo, tanto em casa quanto fora.
    - Eficiência nas finalizações e solidez defensiva (número de clean sheets e gols evitados em situações críticas).

    6. **Situação dos Jogadores-Chave e Condição do Elenco**:
    - Impacto da presença ou ausência de jogadores influentes (artilheiros, principais assistentes, líderes defensivos).
    - Condição física geral do elenco, incluindo possíveis desgastes por calendário apertado, lesões recorrentes e suspensões.

    7. **Estatísticas Avançadas (Expected Goals - xG e Expected Goals Against - xGA)**:
    - xG (qualidade das chances de gol) e xGA (chances de gol permitidas ao adversário) para avaliar a efetividade real de cada time em criar e defender chances.
    - Consistência na conversão de chances em gols e resistência em situações de pressão.

    8. **Estilo de Jogo e Estratégia**:
    - Preferência por estilos específicos (ex: posse de bola, transição rápida, contra-ataque) e suas possíveis vantagens ou desvantagens contra o adversário.
    - Estratégias defensivas e ofensivas do treinador e a capacidade de adaptação a diferentes adversários.

    9. **Condições Ambientais e Estado do Gramado**:
    - Condições climáticas previstas, como chuva, frio, ou calor extremo, que podem favorecer ou prejudicar o desempenho de equipes mais acostumadas com o clima.
    - Estado do gramado (especialmente em partidas fora do país ou em regiões de condições climáticas extremas) que pode favorecer um estilo de jogo físico.

    10. **Odds das Casas de Apostas e Movimentos de Mercado**:
        - Odds iniciais e mudanças recentes, analisando movimentos suspeitos ou aumentos/diminuições significativas nas probabilidades.
        - Interpretação das odds não só como favoritismo, mas como possíveis indicadores de influências externas ou alterações inesperadas.

    11. **Fatores Motivacionais e Situações Internas**:
        - Análise de fatores motivacionais, como rivalidades históricas, trocas recentes de treinador, declarações de jogadores e clima no vestiário.
        - Fatores emocionais ou psicológicos que podem influenciar a performance, como pressão da torcida ou confiança adquirida com bons resultados.

    12. **Calendário e Fadiga Física**:
        - Frequência dos últimos jogos e intervalos de descanso que cada time teve recentemente.
        - Possíveis efeitos da fadiga acumulada, principalmente para times que disputam múltiplas competições ou que viajam longas distâncias.
    13.*Marcadores*
         - Qual time vai marcar o proximo gol 
         - Qual Jogador com maior possibilidade de marcar nessa partida ?

    Utilize esses dados para avaliar as probabilidades de vitória de cada equipe, oferecendo uma recomendação informada e detalhada sobre qual resultado parece mais provável e por quê."""),
        ('user', 'Com base nesses dados, quais são as chances do time X vencer o time Y?')
    ])

    # Invoca o chat com entrada específica
    chain = template | chat
    resposta = chain.invoke({'documentos_informados': documento, 'input': "Qual é o time com maior chance de vencer o próximo jogo e qual é essa porcentagem? Responda apenas com o nome do time e a porcentagem."})

    return resposta.content


while True:
    url = input("Digite a URL (ou 'sair' para encerrar): ")
    if url.lower() == "sair":
        print("Encerrando o programa.")
        break
    elif url.startswith("http://") or url.startswith("https://"):
        resultado = analizar_partida(url)
        print(resultado)
        # Aqui você pode fazer o que precisar com a URL, como armazená-la, processá-la, etc.
    else:
        print("URL inválida. Certifique-se de que comece com 'http://' ou 'https://'.")

