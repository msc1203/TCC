import time
import threading
import random
import numpy as np
#import freenect
import cv2 as cv
from pynput import keyboard  # Se não funcionar, remover import; desabilitar função on_press() e adaptar key_mode()
import RPi.GPIO as GPIO #pip3 install RPi.GPIO
#
## Configurações GPIO
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM) 
## Motor Esquerdo
IN1 = 17  
IN2 = 27
## Motor Direito
IN3 = 23  
IN4 = 24
#
FREQ = 100  # PWM Frequency
TS = 0.05    # Time sleep para ativação do motor
## Configurar os pinos como saída
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

pwm11 = GPIO.PWM(17, FREQ)
pwm21 = GPIO.PWM(27, FREQ)
pwm12 = GPIO.PWM(23, FREQ)
pwm22 = GPIO.PWM(24, FREQ)

# FRENTE -> PWM 11  21 == HIGH  IN1 IN2
# TRAS -> PWM  12  22 == HIGH
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
    #pwm11.stop()
    #pwm21.start(50)
    pwm12.start(50)
    #pwm22.stop()
    # GPIO.output(IN1, GPIO.LOW)
    # GPIO.output(IN2, GPIO.LOW)
    # GPIO.output(IN3, GPIO.HIGH)
    # GPIO.output(IN4, GPIO.LOW)
    time.sleep(TS)
    parar()
    #pwm21.stop()
    #pwm22.stop()
    

def girar_direita():
    #while not stop_event.is_set():
    print("Girando a roda direita")
    #pwm11.start()
    #pwm21.start()
    #pwm12.stop()
    pwm22.start(50)
    # GPIO.output(IN1, GPIO.LOW)
    # GPIO.output(IN2, GPIO.LOW)
    # GPIO.output(IN3, GPIO.LOW)
    # GPIO.output(IN4, GPIO.HIGH)
    time.sleep(TS)
    parar()

def ir_pra_frente():
    #while not stop_event.is_set():
    print("Indo para frente")
    pwm11.start(50)
    pwm21.start(50)
    #pwm12.stop()
    #pwm22.stop()
    # GPIO.output(IN1, GPIO.HIGH)
    # GPIO.output(IN2, GPIO.HIGH)
    # GPIO.output(IN3, GPIO.LOW)
    # GPIO.output(IN4, GPIO.LOW)
    time.sleep(TS)
    parar()
    #pwm11.stop()
    #pwm21.stop()

def ir_pra_tras():
    #while not stop_event.is_set():
    print("Indo para tras")
    #pwm11.stop()
    #pwm21.start(50)
    pwm12.start(50)
    pwm22.start(50)
    # GPIO.output(IN1, GPIO.LOW)
    # GPIO.output(IN2, GPIO.LOW)
    # GPIO.output(IN3, GPIO.HIGH)
    # GPIO.output(IN4, GPIO.HIGH)
    #pwm21.stop()
    #pwm22.stop()
    time.sleep(TS)
    parar()

def parar():
    #while not stop_event.is_set():
    print("Parando motores")
    pwm11.stop()
    pwm21.stop()
    pwm12.stop()
    pwm22.stop()
    # GPIO.output(IN1, GPIO.LOW)
    # GPIO.output(IN2, GPIO.LOW)
    # GPIO.output(IN3, GPIO.LOW)
    # GPIO.output(IN4, GPIO.LOW)
    #time.sleep(1)

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

def auto_mode():
    while True:
        limite_central = 80
        limite_lateral = 80

        depth_data, raw_data = depth_config()
        depth_colored = cv.applyColorMap(depth_data, cv.COLORMAP_JET)
        cv.imshow('Depth Image', depth_colored)
        new_depth_data = get_vector(depth_data)
        analisar_vetor(new_depth_data, limite_central, limite_lateral )
        if cv.waitKey(1) & 0xFF == ord("q"):
            parar()
            return False
        elif cv.waitKey(1) & 0xFF == ord("a"):
            return False
            
def on_press(key):
    try:
        if key.char in ("w", "8"):    # vai para frente
            ir_pra_frente()
        elif key.char in ("s", "2"):  # vai para tras
            ir_pra_tras()
        elif key.char in ("a", "4"):  # gira para a esquerda
            girar_direita()
        elif key.char in ("d", "6"):  # gira para a direita
            girar_esquerda()
        elif key.char in ("p"):        # para os motores
            parar()
        elif key.char == "q":         # troca para modo autonomo
            return False
    except AttributeError:
        pass

        
def key_mode():
    # while True:
        # key = input("Press a key: ")
        # if key == ("w" or "8"):   # Move forward
        #     ir_pra_frente()
        # elif key == ("s" or "2"): # Move Back
        #     ir_pra_tras()
        # elif key == ("a" or "4"): # Move Left
        #     girar_direita()
        # elif key == ("d" or "6"): # Move Right 
        #     girar_esquerda()
        # elif key == "q":
        #     return True

    ## USING KEYBOARD LIBRARY 
    with keyboard.Listener(on_press=on_press) as listener:
        print("on Listener")
        listener.join()  # Keep the program running and listening for key events
    print("Returning true")
    return True

def main():
    mode = False
    parar()
    print("Starting in key mode")
    while True:
        if mode is False:
            print("Im on key mode")
            mode = key_mode()
        elif mode is True:
            print("Im on auto mode")
            GPIO.cleanup()
            parar()
            #mode = auto_mode()

if __name__ == "__main__":
    main()
