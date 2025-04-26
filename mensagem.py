import time
import random
import datetime
import tkinter as tk
from tkinter import messagebox
import winsound
import pywhatkit
import pygame


def tocar_som(caminho_arquivo: str, volume: float = 0.7):
    """
    Toca um som usando pygame.
    
    Parâmetros:
    - caminho_arquivo: str - Caminho para o arquivo de som (.mp3, .wav, etc.)
    - volume: float - Volume do som (0.0 a 1.0)
    """
    pygame.mixer.init()
    pygame.mixer.music.load(caminho_arquivo)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
    
    # Aguarda até o som terminar
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# -----------------------------------------------------------------------------------
# A função abaixo cria uma janela de confirmação utilizando tkinter,
# exibe a mensagem que será enviada e toca um beep padrão do Windows.
# -----------------------------------------------------------------------------------
def confirm_send(message):
    # Cria uma janela oculta principal
    root = tk.Tk()
    root.withdraw()

    # Toca o som padrão (beep) do Windows para chamar a atenção
    winsound.MessageBeep()
    
    # Mostra a mensagem de confirmação
    confirm = messagebox.askyesno("Confirmação de Envio", f"Confirma o envio da mensagem abaixo?\n\n{message}")
    
    root.destroy()
    return confirm

# -----------------------------------------------------------------------------------
# Função para gerar a mensagem com data atual e cobertura variada:
# Se o dia for par, o responsável será 'Evandro', se ímpar, 'Vitor Rigoti'.
# (Você também pode usar random.choice se preferir aleatoriedade completa.)
# -----------------------------------------------------------------------------------
import datetime
import os

def gerar_mensagem():
    hoje = datetime.datetime.now()
    data_str = hoje.strftime("%d/%m")

    caminho_arquivo = "ultimo_responsavel.txt"
    
    # Verifica o último nome usado e alterna
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as f:
            ultimo = f.read().strip()
    else:
        ultimo = "Vitor Rigoti"  # valor inicial

    if ultimo == "Vitor Rigoti":
        coverage_person = "Evandro"
    else:
        coverage_person = "Vitor Rigoti"

    # Salva o novo nome para a próxima vez
    with open(caminho_arquivo, "w") as f:
        f.write(coverage_person)

    mensagem = (
        f"Bom dia!   {data_str}\n\n"
        "Hub Boulevard - equipe completa \n"
        "▪14h Evandro \n"
        "▪15h Vitor Rigoti \n\n"
        f"Cobertura do almoço do líder e/ou assistente {coverage_person}"
    )
    
    return mensagem

# -----------------------------------------------------------------------------------
# 1. Aguarda 5 minutos (300 segundos) após a execução (pode simular o atraso pós login)
# -----------------------------------------------------------------------------------
time.sleep(100)
tocar_som("som/not.mp3")

# -----------------------------------------------------------------------------------
# 2. Gera a mensagem com os dados atuais
# -----------------------------------------------------------------------------------
mensagem = gerar_mensagem()

# -----------------------------------------------------------------------------------
# 3. Exibe a interface de confirmação para o usuário
# -----------------------------------------------------------------------------------
if confirm_send(mensagem):
    # Defina aqui o número de telefone (com DDI e DDD) para o envio, por exemplo: "+5511999999999"
    telefone = "+5543996341638"
    
    # Envia a mensagem instantaneamente pelo WhatsApp Web
    pywhatkit.sendwhatmsg_instantly(telefone, mensagem)
    

    print("Mensagem enviada com sucesso!")
else:
    print("Envio cancelado pelo usuário.")
