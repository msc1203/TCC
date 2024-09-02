import time
import threading
import random
import numpy as np
import freenect
import cv2 as cv
#import RPi.GPIO as GPIO #pip3 install RPi.GPIO
#
## Configurações GPIO
#GPIO.setmode(GPIO.BCM)
## Motor Esquerdo
#IN1 = 17  
#IN2 = 27
## Motor Direito
#IN3 = 23  
#IN4 = 24
## PWM's
#ENA = 22  # PWM para Motor Esquerdo
#ENB = 25  # PWM para Motor Direito
#
## Configurar os pinos como saída
#GPIO.setup(IN1, GPIO.OUT)
#GPIO.setup(IN2, GPIO.OUT)
#GPIO.setup(IN3, GPIO.OUT)
#GPIO.setup(IN4, GPIO.OUT)
#GPIO.setup(ENA, GPIO.OUT)
#GPIO.setup(ENB, GPIO.OUT)
#
## Configurar PWM
#pwm_a = GPIO.PWM(ENA, 1000)  # 1kHz para motor esquerdo
#pwm_b = GPIO.PWM(ENB, 1000)  # 1kHz para motor direito
#pwm_a.start(25)  #duty cycle
#pwm_b.start(25)  #duty cycle

def calcular_media(vetor):
    largura = len(vetor)
    soma = sum(vetor)
    media = soma / largura
    return media

def girar_esquerda():
    #while not stop_event.is_set():
    print("Girando a roda esquerda")
    #GPIO.output(IN1, GPIO.HIGH)
    #GPIO.output(IN2, GPIO.LOW)
    #GPIO.output(IN3, GPIO.LOW)
    #GPIO.output(IN4, GPIO.HIGH)
    time.sleep(4)
    

def girar_direita():
    #while not stop_event.is_set():
    print("Girando a roda direita")
    #GPIO.output(IN1, GPIO.LOW)
    #GPIO.output(IN2, GPIO.HIGH)
    #GPIO.output(IN3, GPIO.HIGH)
    #GPIO.output(IN4, GPIO.LOW)
    time.sleep(4)

def ir_pra_frente():
    #while not stop_event.is_set():
    print("Indo para frente")
    #GPIO.output(IN1, GPIO.HIGH)
    #GPIO.output(IN2, GPIO.LOW)
    #GPIO.output(IN3, GPIO.HIGH)
    #GPIO.output(IN4, GPIO.LOW)
    time.sleep(4)

def parar():
    #while not stop_event.is_set():
    print("Parando motores")
    #GPIO.output(IN1, GPIO.LOW)
    #GPIO.output(IN2, GPIO.LOW)
    #GPIO.output(IN3, GPIO.LOW)
    #GPIO.output(IN4, GPIO.LOW)
    time.sleep(4)

def analisar_vetor(vetor, limite_central, limite_lateral):
    #while not stop_event.is_set():
    tamanho = len(vetor)
    if tamanho < 3:
        print("Vetor muito pequeno para análise")
        return 0
    #
    tercio = tamanho // 3
    #
    parte_esquerda = vetor[:tercio]
    parte_central = vetor[tercio:2*tercio]
    parte_direita = vetor[2*tercio:]
    #
    media_esquerda = calcular_media(parte_esquerda)
    media_central = calcular_media(parte_central)
    media_direita = calcular_media(parte_direita)
    #
    print(f"Média Esquerda: {media_esquerda}, Média Central: {media_central}, Média Direita: {media_direita}")
    #
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
        if media_direita < limite_lateral:
            if media_esquerda < limite_lateral:
                print("Para")
                parar()
            
        elif media_esquerda > media_direita:
            girar_direita()
        else:
            girar_esquerda()

def monitorar_tecla(stop_event):
    input("Pressione 'Enter' para parar...")
    stop_event.set()
    #pwm_a.stop()
    #pwm_b.stop()

def get_vector(vector):
    matriz_sem_colunas = vector[:, 2:-2]
    media_colunas = np.mean(matriz_sem_colunas, axis=0)
    avg_data = media_colunas.reshape(len(media_colunas), 1)
    
    return avg_data

def get_images():
    depth, _ = freenect.sync_get_depth()
    array,_ = freenect.sync_get_video()
    array = cv.cvtColor(array,cv.COLOR_RGB2BGR)

    return depth, array

def depth_config():
    depth, array = get_images()
    depth_scaled = np.uint8(depth / 2048 * 255)
    depth_scaled = depth_scaled[240:, :]

    return depth_scaled, array
        
def main():
    
    
    while True:
        limite_central = 80
        limite_lateral = 80

        depth_data, raw_data = depth_config()
        depth_colored = cv.applyColorMap(depth_data, cv.COLORMAP_JET)
        cv.imshow('Depth Image', depth_colored)
        new_depth_data = get_vector(depth_data)
        analisar_vetor(new_depth_data,limite_central, limite_lateral )

        if cv.waitKey(1) & 0xFF == ord("q"):
            parar()
            break

if __name__ == "__main__":
    main()
