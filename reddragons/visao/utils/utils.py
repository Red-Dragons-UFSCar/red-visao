import numpy as np
import cv2
import math

def converte_coord (matriz, coord):
    """encontra o valor da coordenada apos a transformacao de perspectiva

    Args:
        matriz (np.array): matriz warp
        coord ((int,int)): coordenada a ser convertida

    Returns:
        (int,int): coordenada convertida
    """
    new = np.matmul(matriz, list(coord)+[1])
    return tuple(np.int32([new[0], new[1]]/new[2]))

def corteImagem(fonte, dados):
    tamanho = dados.size
    
    imagem = fonte
    
    supEsquerdo = dados.corte[0]
    imagem[0:supEsquerdo[1], 0:supEsquerdo[0], :] = 0
    imagem[0:dados.corte[1][1], dados.corte[1][0]:640, :] = 0
    imagem[dados.corte[2][1]:480, 0:dados.corte[2][0], :] = 0
    imagem[dados.corte[3][1]:480, dados.corte[3][0]:640, :] = 0
    
    return imagem

def matriz_warpPerspective(dados):
    size = dados.size
    W = size[0]
    H = size[1]
    
    src = np.float32(dados.warpPerspective)
    dst = np.float32([[0,0], [W,0], [0,H], [W,H]])
    M = cv2.getPerspectiveTransform(src, dst)
    return M
    
def warpPerspective(imagem, dados):
    size = dados.size
    M = dados.M_warpPerspective
    
    destino = cv2.warpPerspective(imagem, M, (size[0],size[1]))
    return destino
    
def getContornoCor(imagemHSV, cor, filtro):
    if cor[0][0] > cor[1][0]:
        aux = np.copy(cor[0])
        aux[0] = 0
        mascara1 = cv2.inRange(imagemHSV, aux, cor[1])
        
        aux = np.copy(cor[1])
        aux[0] = 179
        mascara2 = cv2.inRange(imagemHSV, cor[0], aux)
        
        mascara = cv2.bitwise_or(mascara1, mascara2)
    else:
        mascara = cv2.inRange(imagemHSV, cor[0], cor[1])
        
    matrizFiltro = None
    if filtro[1] == 0:
        matrizFiltro = np.ones((filtro[2], filtro[2]), np.uint8)
        
    if filtro[1] == 1:
        matrizFiltro = np.zeros((filtro[2], filtro[2]), np.uint8)
        meio = int((filtro[2]-1)/2)
        for i in range(filtro[2]):
            matrizFiltro[i, meio] = 1
            matrizFiltro[meio, i] = 1
    
    if matrizFiltro is not None and filtro[0] == 1:
        resultado = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, matrizFiltro)
    
    elif matrizFiltro is not None and filtro[0] == 2:
        resultado = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, matrizFiltro)
        
    else:
        resultado = mascara
        
    contornos, hierarquia = cv2.findContours(resultado,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    return contornos, hierarquia
    
def centroRobo(princ, sec, angCorr = 90):
    meioX = (princ[0] + sec[0])/2
    meioY = (princ[1] + sec[1])/2
    ang = math.atan2(princ[1] - sec[1], princ[0] - sec[0])
    angulo = ang + angCorr
    return meioX, meioY, angulo
    
def calculaCentros(D, angCorr = 90):
    centros = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i_sec in range(2, 5):
        menor = 10000.0
        for principal in D[1][0]:
            try:
                for secundario in D[i_sec][0]:
                    dist = math.hypot(principal[0] - secundario[0], principal[1] - secundario[1])
                    if dist < menor:
                        menor = dist
                        mX, mY, ang = centroRobo(principal, secundario, angCorr)
                        centros[i_sec - 2][0] = mX
                        centros[i_sec - 2][1] = mY
                        centros[i_sec - 2][2] = ang
                        
            except:
                pass
    return centros