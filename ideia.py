import time
import threading
import random
import keyboard

def calcular_media(vetor):
    """Função para calcular a média dos valores em um vetor."""
    return sum(vetor) / len(vetor) if vetor else 0

def girar_esquerda():
    """Função para simular a ação de girar à esquerda."""
    print("Girando à esquerda")

def girar_direita():
    """Função para simular a ação de girar à direita."""
    print("Girando à direita")

def ir_pra_frente(stop_event):
    """Função para simular a ação de ir para frente."""
    while not stop_event.is_set():
        print("Indo para frente")
        time.sleep(1)  # Simula a ação contínua de ir para frente

def analisar_vetor(vetor, limite_inferior, limite_lateral, intervalo, stop_event):
    """Função para analisar as médias das partes do vetor em intervalos de tempo."""
    while not stop_event.is_set():
        tamanho = len(vetor)
        if tamanho < 3:
            print("Vetor muito pequeno para análise")
            break

        tercio = tamanho // 3

        parte_esquerda = vetor[:tercio]
        parte_central = vetor[tercio:2*tercio]
        parte_direita = vetor[2*tercio:]

        media_esquerda = calcular_media(parte_esquerda)
        media_central = calcular_media(parte_central)
        media_direita = calcular_media(parte_direita)

        print(f"Média Esquerda: {media_esquerda}, Média Central: {media_central}, Média Direita: {media_direita}")

        if media_central > limite_inferior:
            if media_direita > limite_lateral:
                girar_esquerda()

            if media_esquerda > limite_lateral:
                girar_direita()
        else:
            print("Obstáculo a frente")
            if media_direita > media_esquerda:
                girar_esquerda()
            else:
                girar_direita()

        time.sleep(intervalo)  # Aguarda pelo período especificado antes da próxima iteração

def atualizar_vetor(vetor, stop_event):
    """Função para atualizar os valores do vetor de forma aleatória."""
    while not stop_event.is_set():
        for i in range(len(vetor)):
            vetor[i] = random.randint(1, 100)  # Gera um valor aleatório entre 1 e 100
        print(f"Vetor atualizado: {vetor}")
        time.sleep(intervalo)  # Simula um intervalo de tempo para atualização do vetor

def monitorar_tecla(stop_event):
    """Função para monitorar o pressionamento de uma tecla."""
    print("Pressione 'q' para parar.")
    keyboard.wait('q')
    stop_event.set()

# Exemplo de uso
vetor_distancias = [60, 36, 81, 91, 98, 56, 93, 76, 57, 50, 45, 20]
limite_inferior = 40
limite_lateral = 30 # valor limite de proximidade
intervalo = 5  # Intervalo de 1 segundo entre cada análise

# Cria um evento para sinalizar a parada
stop_event = threading.Event()

# Inicia a função ir_pra_frente em um thread separado
thread_ir_pra_frente = threading.Thread(target=ir_pra_frente, args=(stop_event,))
thread_ir_pra_frente.daemon = True
thread_ir_pra_frente.start()

# Inicia a análise do vetor em um thread separado
thread_analisar_vetor = threading.Thread(target=analisar_vetor, args=(vetor_distancias, limite_inferior, limite_lateral, intervalo, stop_event))
thread_analisar_vetor.start()

# Inicia a atualização do vetor em um thread separado
thread_atualizar_vetor = threading.Thread(target=atualizar_vetor, args=(vetor_distancias, stop_event))
thread_atualizar_vetor.start()

# Inicia a monitorização do pressionamento da tecla 'q'
monitorar_tecla(stop_event)

# Espera a análise do vetor e a atualização do vetor terminar
thread_analisar_vetor.join()
thread_atualizar_vetor.join()

print("Programa encerrado.")
