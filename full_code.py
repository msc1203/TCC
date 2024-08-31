import time
import threading
import random
import numpy as np
import freenect
import RPi.GPIO as GPIO #pip3 install RPi.GPIO

# Configurações GPIO
GPIO.setmode(GPIO.BCM)
# Motor Esquerdo
IN1 = 17  
IN2 = 27
# Motor Direito
IN3 = 23  
IN4 = 24
# PWM's
ENA = 22  # PWM para Motor Esquerdo
ENB = 25  # PWM para Motor Direito

# Configurar os pinos como saída
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Configurar PWM
pwm_a = GPIO.PWM(ENA, 1000)  # 1kHz para motor esquerdo
pwm_b = GPIO.PWM(ENB, 1000)  # 1kHz para motor direito
pwm_a.start(25)  #duty cycle
pwm_b.start(25)  #duty cycle

def calcular_media(vetor):
    largura = len(vetor)
    soma = sum(vetor)
    media = soma / largura
    return media

def girar_esquerda():
    print("Girando a roda esquerda")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(4)
    

def girar_direita():
    print("Girando a roda direita")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(4)

def ir_pra_frente(stop_event):
    while not stop_event.is_set():
        print("Indo para frente")
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        time.sleep(4)

def analisar_vetor(vetor, limite_central, limite_lateral, intervalo, stop_event):
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

        if media_central > limite_central:
            print("Caminho livre a frente")
            if media_direita > media_esquerda:
                if media_esquerda < limite_lateral:
                    girar_esquerda()
                else:
                    print("Continue em frente")
            elif media_direita < media_esquerda:
                if media_direita < limite_lateral:
                    girar_direita()
                else:
                    print("Continue em frente")
        else:
            print("Obstáculo a frente")
            if media_direita > media_esquerda:
                girar_esquerda()
            else:
                girar_direita()

        time.sleep(intervalo)

def atualizar_vetor(vetor, stop_event, intervalo):
    while not stop_event.is_set():
        for i in range(len(vetor)):
            vetor[i] = random.randint(20, 60)
        time.sleep(intervalo)

def monitorar_tecla(stop_event):
    input("Pressione 'Enter' para parar...")
    stop_event.set()
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()

def get_vector():
    depth, _ = freenect.sync_get_depth()
    vector = depth * 0.001
    #vector = np.random.randint(20, 150, (240, 320), dtype=np.uint8)
    matriz_sem_colunas = vector[:, 1:-1]
    media_colunas = np.mean(matriz_sem_colunas, axis=0)
    vector = media_colunas.reshape(len(media_colunas), 1)
    return vector

def main():
    limite_central = 30
    limite_lateral = 30
    intervalo = 5

    vetor_distancias = get_vector()

    stop_event = threading.Event()

    thread_ir_pra_frente = threading.Thread(target=ir_pra_frente, args=(stop_event,))
    thread_ir_pra_frente.daemon = True
    thread_ir_pra_frente.start()

    thread_analisar_vetor = threading.Thread(target=analisar_vetor, args=(vetor_distancias, limite_central, limite_lateral, intervalo, stop_event))
    thread_analisar_vetor.start()

    thread_atualizar_vetor = threading.Thread(target=atualizar_vetor, args=(vetor_distancias, stop_event, intervalo))
    thread_atualizar_vetor.start()

    thread_monitorar_tecla = threading.Thread(target=monitorar_tecla, args=(stop_event,))
    thread_monitorar_tecla.start()

    thread_analisar_vetor.join()
    thread_atualizar_vetor.join()

    if stop_event.is_set():
        print("Encerrando programa...")

if __name__ == "__main__":
    main()
