#

import numpy as np
from math import *
from controle import controle
from verificaControle import atingiuAngulo
from enviarInfo import *
import enviarInfo

"""
Função:  posicaoInicial
Objetivo: Tem a função de posicionar os robôs nas respectivas posições iniciais do jogo

Parametros de entrada:
    # RD - matriz 3x3, sendo:
    [0,X] - Coordenada X do robô; [1,X] - Coordenada Y do robô; [2,X] - angulo do robô
    # bola - vetor de 2 posições, sendo:
    [0] - Coordenada X da bola; [1] - Coordenada Y da bola
    # ser - Porta serial (em caso de não haver comunicador conectado, passar 0)
    # constX e constY - Constantes para transformar pixels em metros
    # ambienteReal - Variavel booleana responsável por ativar a simulação ou escrita na porta serial     
    # duasFaces - Variavel booleana responsável por ativar as duas frentes do robô
    # trocouCampo - Variavel booleana responsável por informar qual o lado do campo que está o jogo corrente
    # debug - Faz, em tempo de execução, exibir dados relevantes no terminal
    # clientID - Criado na main (caso ambienteReal seja verdadeiro, fazer clientID = 0)

Retorno:
    Sem retorno
"""
def posicaoInicial(RD, bola, ser, constX, constY, ambienteReal, duasFaces, trocouCampo, bolaNossa, debug, clientID):
    #dadosR - 0 posição X do robô; 1 posição Y do robô; 2 angulo do robô; 3 KP; 4 velocidade máxima; 5 função do robo (0-goleiro; 1-zagueiro; 2-atacante); 6 código do robô (0-@; 1-&; 2-!)
    dadosR = np.zeros([3, 7])
    alvoR1 = np.zeros([3])
    alvoR2 = np.zeros([3])
    alvoR3 = np.zeros([3])

    #0 posição X; 1 posição Y; 2 angulo; 3 KP; 4 velocidade máxima; 5 função do robo (0-goleiro; 1-zagueiro; 2-atacante); 6 código do robô (0-@; 1-&; 2-!)
    if (not ambienteReal):
        dadosR[0] = RD[0,0] * constX, RD[0,1] * constY, RD[0,2], 2.5, 10, 0, 0
        dadosR[1] = RD[1,0] * constX, RD[1,1] * constY, RD[1,2], 2.5, 10, 1, 1
        dadosR[2] = RD[2,0] * constX, RD[2,1] * constY, RD[2,2], 2.5, 10, 2, 2 
    else:
        dadosR[0] = RD[0,0] * constX, RD[0,1] * constY, RD[0,2], 18, 200, 0, 0
        dadosR[1] = RD[1,0] * constX, RD[1,1] * constY, RD[1,2], 18, 200, 1, 1
        dadosR[2] = RD[2,0] * constX, RD[2,1] * constY, RD[2,2], 18, 200, 2, 2

        
    if trocouCampo and (bolaNossa == 1):
        alvoR1 = [150, 65]
        alvoR2 = [115, 75]
        alvoR3 = [95, 55]

    elif ((not trocouCampo) and (bolaNossa == 1)):
        alvoR1 = [15, 65]
        alvoR2 = [60, 75]
        alvoR3 = [75, 55]
    
    elif (trocouCampo and (bolaNossa == 0)):
        alvoR1 = [150, 65]
        alvoR2 = [115, 75]
        alvoR3 = [115, 55]

    elif ((not trocouCampo) and (bolaNossa == 0)):
        alvoR1 = [15, 65]
        alvoR2 = [60, 75]
        alvoR3 = [60, 55]
            
    controle(dadosR[0], alvoR1, ser, ambienteReal, duasFaces, debug, clientID)
    controle(dadosR[1], alvoR2, ser, ambienteReal, duasFaces, debug, clientID)
    controle(dadosR[2], alvoR3, ser, ambienteReal, duasFaces, debug, clientID)


"""
Função:  parada
Objetivo: A função parada tem objetivo de enviar aos robôs a velocidade zero para todas as rodas, parando o robô.

Parametros de entrada:

    # RD -  matriz 3x3, sendo:
    [0,X] - Coordenada X do robô; [1,X] - Coordenada Y do robô; [2,X] - angulo do robô
    # bola - vetor de 2 posições, sendo:
    [0] - Coordenada X da bola; [1] - Coordenada Y da bola
    # ser -  Porta serial (em caso de não haver comunicador conectado, passar 0)
    # constX e constY - Constantes para transformar pixels em metros
    # ambienteReal - Variavel booleana responsável por ativar a simulação ou escrita na porta serial     
    # duasFaces - Variavel booleana responsável por ativar as duas frentes do robô
    # trocouCampo - Variavel booleana responsável por informar qual o lado do campo que está o jogo corrente
    # debug - Faz, em tempo de execução, exibir dados relevantes no terminal
    # clientID - Criado na main (caso ambienteReal seja verdadeiro, fazer clientID = 0)

Retorno:
    Sem retorno
"""
def parada(RD, bola, ser, constX, constY, ambienteReal, duasFaces, trocouCampo, debug, clientID):
    #dadosR - 0 posição X do robô; 1 posição Y do robô; 2 angulo do robô; 3 KP; 4 velocidade máxima; 5 função do robo (0-goleiro; 1-zagueiro; 2-atacante); 6 código do robô (0-@; 1-&; 2-!)
    dadosR = np.zeros([3, 7])
     #0 posição X; 1 posição Y; 2 angulo; 3 KP; 4 velocidade máxima; 5 função do robo (0-goleiro; 1-zagueiro; 2-atacante); 6 código do robô (0-@; 1-&; 2-!)
    if (not ambienteReal):
        dadosR[0] = RD[0,0] * constX, RD[0,1] * constY, RD[0,2], 3, 10, 0, 0
        dadosR[1] = RD[1,0] * constX, RD[1,1] * constY, RD[1,2], 3, 10, 1, 1
        dadosR[2] = RD[2,0] * constX, RD[2,1] * constY, RD[2,2], 3, 10, 2, 2 
    else:
        dadosR[0] = RD[0,0] * constX, RD[0,1] * constY, RD[0,2], 18, 300, 0, 0
        dadosR[1] = RD[1,0] * constX, RD[1,1] * constY, RD[1,2], 18, 300, 1, 1
        dadosR[2] = RD[2,0] * constX, RD[2,1] * constY, RD[2,2], 18, 300, 2, 2 

    enviarInfo.dados_controle(dadosR[0], ser, 0, 0, 0, 0, ambienteReal, clientID, debug)
    enviarInfo.dados_controle(dadosR[1], ser, 0, 0, 0, 0, ambienteReal, clientID, debug)
    enviarInfo.dados_controle(dadosR[2], ser, 0, 0, 0, 0, ambienteReal, clientID, debug)


'''
Função: correção angulo
Objetivo: Corrigir o angulo do robô até atingir o angulo desejado
'''
def corrigirangulo(RD, angulodesejado, ser, constX, constY, ambienteReal, debug, clientID):
     #dadosR - 0 posição X do robô; 1 posição Y do robô; 2 angulo do robô; 3 KP; 4 velocidade máxima; 5 função do robo (0-goleiro; 1-zagueiro; 2-atacante); 6 código do robô (0-@; 1-&; 2-!)
    dadosR = np.zeros([3, 7])
     #0 posição X; 1 posição Y; 2 angulo; 3 KP; 4 velocidade máxima; 5 função do robo (0-goleiro; 1-zagueiro; 2-atacante); 6 código do robô (0-@; 1-&; 2-!)
    if (not ambienteReal):
        dadosR[0] = RD[0,0] * constX, RD[0,1] * constY, RD[0,2], 3, 10, 0, 0
        dadosR[1] = RD[1,0] * constX, RD[1,1] * constY, RD[1,2], 3, 10, 1, 1
        dadosR[2] = RD[2,0] * constX, RD[2,1] * constY, RD[2,2], 3, 10, 2, 2 
    else:
        dadosR[0] = RD[0,0] * constX, RD[0,1] * constY, RD[0,2], 18, 300, 0, 0
        dadosR[1] = RD[1,0] * constX, RD[1,1] * constY, RD[1,2], 18, 300, 1, 1
        dadosR[2] = RD[2,0] * constX, RD[2,1] * constY, RD[2,2], 18, 300, 2, 2 
    if (not (atingiuAngulo(dadosR[0], angulodesejado, 0.17) or atingiuAngulo(dadosR[1], angulodesejado, 0.17) or atingiuAngulo(dadosR[2], angulodesejado, 0.17)) ):
        enviarInfo.dados_controle(dadosR[0], ser, dadosR[0,4]*0.3, dadosR[0,4]*0.3, 0, 1, ambienteReal, clientID, debug)
        enviarInfo.dados_controle(dadosR[1], ser, dadosR[1,4]*0.3, dadosR[1,4]*0.3, 0, 1, ambienteReal, clientID, debug)
        enviarInfo.dados_controle(dadosR[2], ser, dadosR[2,4]*0.3, dadosR[2,4]*0.3, 0, 1, ambienteReal, clientID, debug)
'''
Função: fazer semicirculo com relação a posição da bola
Objetivo: Descreve uma semicírculo entorno do vetor centro (x,y) com determinado raio enrelação ao movimento da bola
Retorna: Alvo do robô
'''
def fazerSemicirculo(bola,centro,raio):
    #alvo(x,y)
    alvo = np.zeros(2)
    #distancia entre a bola e o centro
    d = sqrt((bola[0] - centro[0])**2 + (bola[1] - centro[1])**2)
    #angulo entre o centro e a bola
    teta = acos(abs(bola[1] - centro[1]) / d)
    #Verificação se a bola está acima ou abaixo do centro
    if(bola[1] <= centro[1]):
        #Decomposição do vetor entre o centro com tamanho do raio
        alvo[0] = abs(centro[0] - sin(teta)*raio)
        alvo[1] = abs(centro[1] - cos(teta)*raio)

    else:
        #Decomposição do vetor entre o centro com tamanho do raio
        alvo[0] = abs(centro[0] - sin(teta)*raio)
        alvo[1] = abs(centro[1] + cos(teta)*raio)

    return alvo

'''
Função: Seguir no Eixo Y
Objetivo: Copia a posição Y da bola em determinado ponto em x, podendo definir limites para o movimento em Y
Retorna: Alvo do robô
'''
def seguirEixoY(bola,pontoX,pontosLimite):
    alvo = np.zeros(2)

    alvo[0] = pontoX
    #Verifica se a bola esta abaixo ou acima do limite e define o máximo
    if(bola[1] < pontosLimite[0]):
        alvo[1] = pontosLimite[0] + 1

    elif(bola[1] > pontosLimite[1]):
        alvo[1] = pontosLimite[1] - 1

    else:
        alvo[1] = bola[1]

    return alvo

'''
Função: Seguir Alvo
Objetivo: Definir a posição da bola como alvo
Retorna: Alvo do robô
'''
def seguirAlvo(bola):
    alvo = np.zeros(2)

    alvo = bola

    return alvo