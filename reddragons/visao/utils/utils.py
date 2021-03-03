import numpy as np

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