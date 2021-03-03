import numpy as np
import math

#Calculo do angulo desejado
def calculaAngulo(origem, destino):
    delta_x = origem[0] - destino[0]
    delta_y = origem[1] - destino[1]
    angulo = np.arctan2(delta_y,delta_x)
    return angulo


#Calculo da distancia entre dois pontos
def distancia(pontoa, pontob):
    dist = math.sqrt((pontoa[0] - pontob[0])**2 + (pontoa[1] - pontob[1])**2)
    return dist
