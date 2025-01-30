import threading
import random
import time


tablero = [' ' for _ in range(9)]

def imprimir_tablero():
    print(f'{tablero[0]} | {tablero[1]} | {tablero[2]}')
    print('---------')
    print(f'{tablero[3]} | {tablero[4]} | {tablero[5]}')
    print('---------')
    print(f'{tablero[6]} | {tablero[7]} | {tablero[8]}')


def verificar_ganador(jugador):
    combinaciones_ganadoras = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for combinacion in combinaciones_ganadoras:
        if tablero[combinacion[0]] == tablero[combinacion[1]] == tablero[combinacion[2]] == jugador:
            return True
    return False

def jugador1():
    while True:
      
        posicion = random.randint(0, 8)
        if tablero[posicion] == ' ':
            tablero[posicion] = 'X'
            imprimir_tablero()
            if verificar_ganador('X'):
                print('Jugador 1 gana!')
                exit()
        time.sleep(1)

def jugador2():
    while True:
       
        posicion = random.randint(0, 8)
        if tablero[posicion] == ' ':
            tablero[posicion] = 'O'
            imprimir_tablero()
            if verificar_ganador('O'):
                print('Jugador 2 gana!')
                exit()
        time.sleep(1)


t1 = threading.Thread(target=jugador1)
t2 = threading.Thread(target=jugador2)


t1.start()
t2.start()