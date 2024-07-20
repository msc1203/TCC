import time
import threading
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
        time.sleep(0.1)  # Simula a ação contínua de ir para frente

def analisar_vetor(vetor, limite_inferior, limite_lateral, intervalo, stop_event):
    """Função para analisar as médias das partes do vetor em intervalos de tempo."""
    tamanho = len(vetor)
    if tamanho < 3:
        print("Vetor muito pequeno para análise")
        return

    tercio = tamanho // 3

    while not stop_event.is_set():
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
            if media_direita > media_esquerda:
                girar_esquerda()
            else:
                girar_direita()

        # Simulação de atualização do vetor para a próxima iteração
        # No exemplo real, o vetor deveria ser atualizado com novos valores
        vetor = [v - 1 if v > 0 else v for v in vetor]  # Exemplo de decrementar todas as distâncias para simulação
        if all(v <= 0 for v in vetor):  # Condição de parada para evitar loop infinito na simulação
            break

        time.sleep(intervalo)  # Aguarda pelo período especificado antes da próxima iteração

def monitorar_tecla(stop_event):
    """Função para monitorar o pressionamento de uma tecla."""
    print("Pressione 'q' para parar.")
    keyboard.wait('q')
    stop_event.set()

# Exemplo de uso
vetor_distancias = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
limite_inferior = 4
limite_lateral = 6
intervalo = 1  # Intervalo de 1 segundo entre cada análise

# Cria um evento para sinalizar a parada
stop_event = threading.Event()

# Inicia a função ir_pra_frente em um thread separado
thread_ir_pra_frente = threading.Thread(target=ir_pra_frente, args=(stop_event,))
thread_ir_pra_frente.daemon = True
thread_ir_pra_frente.start()

# Inicia a análise do vetor em um thread separado
thread_analisar_vetor = threading.Thread(target=analisar_vetor, args=(vetor_distancias, limite_inferior, limite_lateral, intervalo, stop_event))
thread_analisar_vetor.start()

# Inicia a monitorização do pressionamento da tecla 'q'
monitorar_tecla(stop_event)

# Espera a análise do vetor terminar
thread_analisar_vetor.join()

print("Programa encerrado.")
