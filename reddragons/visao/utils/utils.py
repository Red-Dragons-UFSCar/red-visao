import math
from pathlib import Path

import cv2
import numpy as np
from reddragons.visao.logger import Logger

__all__ = [
    'VIDEO_PATH',
    'converte_coord',
    'test_device',
    'corte_imagem',
    'matriz_warp_perspective',
    'warp_perspective',
    'get_contorno_cor',
    'centro_robo',
    'calcula_centros',
    'checar_erro_centroide',
]
#constantes
VIDEO_PATH = str(Path(__file__, "../../../../data/jogo.avi").resolve())

#funcoes
def converte_coord(matriz, coord):
    """encontra o valor da coordenada apos a transformacao de perspectiva

    Args:
        matriz (np.array): matriz warp
        coord ((int,int)): coordenada a ser convertida

    Returns:
        (int,int): coordenada convertida
    """
    new = np.matmul(matriz, list(coord) + [1])
    return tuple(np.int32([new[0], new[1]] / new[2]))

def test_device(src):
    cap = cv2.VideoCapture(src)
    if cap is None or not cap.isOpened():
        Logger().erro("Não foi possível abrir o dispositivo: " + str(src))
        return 0
    return 1

def corte_imagem(fonte, dados):
    imagem = fonte

    sup_esquerdo = dados.corte[0]
    imagem[0 : sup_esquerdo[1], 0 : sup_esquerdo[0], :] = 0
    imagem[0 : dados.corte[1][1], dados.corte[1][0] : 640, :] = 0
    imagem[dados.corte[2][1] : 480, 0 : dados.corte[2][0], :] = 0
    imagem[dados.corte[3][1] : 480, dados.corte[3][0] : 640, :] = 0

    return imagem


def matriz_warp_perspective(dados):
    size = dados.size
    width = size[0]
    height = size[1]

    src = np.float32(dados.warp_perspective)
    dst = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matriz = cv2.getPerspectiveTransform(src, dst)
    return matriz


def warp_perspective(imagem, dados):
    size = dados.size
    matriz = dados.matriz_warp_perspective

    destino = cv2.warpPerspective(imagem, matriz, (size[0], size[1]))
    return destino


def get_contorno_cor(imagem_hsv, cor, filtro):
    if cor[0][0] > cor[1][0]:
        aux = np.copy(cor[0])
        aux[0] = 0
        mascara1 = cv2.inRange(imagem_hsv, aux, cor[1])

        aux = np.copy(cor[1])
        aux[0] = 179
        mascara2 = cv2.inRange(imagem_hsv, cor[0], aux)

        mascara = cv2.bitwise_or(mascara1, mascara2)
    else:
        mascara = cv2.inRange(imagem_hsv, cor[0], cor[1])

    matriz_filtro = None
    if filtro[1] == 0:
        matriz_filtro = np.ones((filtro[2], filtro[2]), np.uint8)

    if filtro[1] == 1:
        matriz_filtro = np.zeros((filtro[2], filtro[2]), np.uint8)
        meio = int((filtro[2] - 1) / 2)
        for i in range(filtro[2]):
            matriz_filtro[i, meio] = 1
            matriz_filtro[meio, i] = 1

    if matriz_filtro is not None and filtro[0] == 1:
        resultado = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, matriz_filtro)

    elif matriz_filtro is not None and filtro[0] == 2:
        resultado = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, matriz_filtro)

    else:
        resultado = mascara

    contornos, hierarquia = cv2.findContours(
        resultado, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    return contornos, hierarquia


def centro_robo(princ, sec, ang_corr=90):
    meio_x = (princ[0] + sec[0]) / 2
    meio_y = (princ[1] + sec[1]) / 2
    ang = math.atan2(princ[1] - sec[1], princ[0] - sec[0])
    angulo = ang + ang_corr
    return meio_x, meio_y, angulo


def calcula_centros(centroids, ang_corr=90):
    centros = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i_sec in range(2, 5):
        menor = 10000.0
        for principal in centroids[1][0]:
            try:
                for secundario in centroids[i_sec][0]:
                    dist = math.hypot(
                        principal[0] - secundario[0], principal[1] - secundario[1]
                    )
                    if dist < menor:
                        menor = dist
                        m_x, m_y, ang = centro_robo(principal, secundario, ang_corr)
                        centros[i_sec - 2][0] = m_x
                        centros[i_sec - 2][1] = m_y
                        centros[i_sec - 2][2] = ang
            except ValueError:
                pass
    return centros

def checar_erro_centroide(centros):
    erros = [0, 0, 0]
    i = 0

    for c in centros:
        if c[0] == 0 or c[1] == 0:
            erros[i] += 1
            Logger().erro("Um centro não detectado")
        i += 1
    return erros
