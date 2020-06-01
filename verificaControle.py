# -*- coding: utf-8 -*-
"""
@Data:          06/Fevereiro/2019
@Objetivo:      Funções para verificar posição e angulo dos jogadores
@Autor:         RED DRAGONS UFSCAR - Divisão controle e estratégia
@Membros:       Alexandre Dias Negretti
                Carlos Basali
                George Maneta
                Marcos Augusto Faglioni Junior 
                Natália dos Santos Andrade
                Vinicius Ancheschi Strini
"""
from math import *
import numpy as np
import math
import calculaControle
"""
Função:  atingiuAlvo
Objetivo: Verificar se o robô esta dentro de uma circunferência de raio erro com o centro no alvo

Parametros de entrada:
    ## RD ## Vetor de 6 posições, sendo:
    [0] - Coordenada X do robô; [1] - Coordenada Y do robô; [2] - angulo do robô; [3] - KP (constante de controle);
    [4] - velocidade máxima;    [5] - Função do robo (0-goleiro; 1-zagueiro; 2-atacante); [6] - Código do robô (0 -> @; 1 -> &; 2 -> $)

    ## alvo ## vetor de 2 posições, sendo:
    [0] - Coordenada X do alvo; [1] - Coordenada Y do alvo

    ## erro ## Valor em centimetros que representa o raio da circunferência com centro em alvo

Retorno:
    "True" ou "False"
    Variável booleana indicando se o robô está em um raio de erro centimetros do ponto desejado (verdadeiro se estiver no raio e falso caso contrário)

"""
def atingiuAlvo(RD, alvo, erro):
    temp = math.sqrt((alvo[0] - RD[0]) ** 2 + (alvo[1] - RD[1]) ** 2)
    return temp < erro

"""
Função:  atingiuAlvoY
Objetivo: Verificar se o robô esta dentro de uma circunferência de raio erro com o centro no alvo

Parametros de entrada:
    ## RD ## Vetor de 6 posições, sendo:
    [0] - Coordenada X do robô; [1] - Coordenada Y do robô; [2] - angulo do robô; [3] - KP (constante de controle);
    [4] - velocidade máxima;    [5] - Função do robo (0-goleiro; 1-zagueiro; 2-atacante); [6] - Código do robô (0 -> @; 1 -> &; 2 -> $)

    ## alvo ## vetor de 2 posições, sendo:
    [0] - Coordenada X do alvo; [1] - Coordenada Y do alvo

    ## erro ## Valor em centimetros que representa o raio da circunferência com centro em alvo

Retorno:
    "True" ou "False"
    Variável booleana indicando se o robô está em um raio de erro centimetros do ponto desejado (verdadeiro se estiver no raio e falso caso contrário)

"""
def atingiuAlvoY(RD, alvo, erro):
    temp = math.sqrt((alvo[1] - RD[1]) ** 2)
    return temp < erro

"""
Função:  atingiuAngulo
Objetivo: Verificar se o robô atingiu o angulo desejado, a menos de um erro

Parametros de entrada:
    ## RD ## Vetor de 6 posições, sendo:
    [0] - Coordenada X do robô; [1] - Coordenada Y do robô; [2] - angulo do robô; [3] - KP (constante de controle);
    [4] - velocidade máxima;    [5] - Função do robo (0-goleiro; 1-zagueiro; 2-atacante); [6] - Código do robô (0 -> @; 1 -> &; 2 -> $)

    ## anguloDesejado ## Ângulo desejado em radianos

    ## erro ## Valor em radianos que representa o erro máximo para ser considerado

Retorno:
    "True" ou "False"
    Variável booleana indicando se o robô está a menos de erro do ângulo desejado
"""
def atingiuAngulo(RD, anguloDesejado, erro):
    temp = math.sqrt((RD[2] - anguloDesejado) ** 2)
    return temp < erro


def estaNaBordaInferior(RD, tamanhoBorda):    #Na simulação é a borda superior    
    if(RD[1] > 130 - tamanhoBorda):
        return True
    else:
        return False


def estaNaBordaSuperior(RD, tamanhoBorda):    #Na simulação é a borda inferior      
    if(RD[1] < tamanhoBorda):
        return True
    else:
        return False


def estaNaBordaInferiorGolEsq(RD, tamanhoBorda):    #Na simulação é a borda esquerda acima do gol            
    if(RD[0] < tamanhoBorda and RD[1] > 85 and RD[1] < 130 - tamanhoBorda):
        return True
    else:
        return False


def estaNaBordaInferiorGolDir(RD, tamanhoBorda):    #Na simulação é a borda direita acima do gol            
    if(RD[0] > 168 - tamanhoBorda and RD[1] > 85 and RD[1] < 130 - tamanhoBorda):
        return True
    else:
        return False


def estaNaBordaSuperiorGolEsq(RD, tamanhoBorda):     #Na simulação é a borda esquerda abaixo do gol           
    if(RD[0] < tamanhoBorda and RD[1] < 45 and RD[1] > tamanhoBorda):
        return True
    else:
        return False


def estaNaBordaSuperiorGolDir(RD, tamanhoBorda):    #Na simulação é a borda direita abaixo do gol            
    if(RD[0] > 168 - tamanhoBorda and RD[1] < 45 and RD[1] > tamanhoBorda):
        return True
    else:
        return False
        
def estaNaBorda(RD,tamanhoBorda):
    #Criação das variaveis utilizadas nas função
    global estaNaBordaSuperior
    global estaNaBordaInferior
    global estaNaBordaSuperiorGolDir
    global estaNaBordaSuperiorGolEsq
    global estaNaBordaInferiorGolDir
    global estaNaBordaInferiorGolEsq
    if(RD[1] > 130 - tamanhoBorda):
        estaNaBordaInferior=True
        return True,estaNaBordaInferior
    elif(RD[1] < tamanhoBorda):
        estaNaBordaSuperior=True
        return True,estaNaBordaSuperior
    elif(RD[0] < tamanhoBorda and RD[1] > 85 and RD[1] < 130 - tamanhoBorda):
        estaNaBordaInferiorGolEsq=True
        return True,estaNaBordaInferiorGolEsq
    elif(RD[0] > 168 - tamanhoBorda and RD[1] > 85 and RD[1] < 130 - tamanhoBorda):
        estaNaBordaInferiorGolDir=True
        return True,estaNaBordaInferiorGolDir
    elif(RD[0] < tamanhoBorda and RD[1] < 45 and RD[1] > tamanhoBorda):
        estaNaBordaSuperiorGolEsq=True
        return True,estaNaBordaInferiorGolDir
    elif(RD[0] > 168 - tamanhoBorda and RD[1] < 45 and RD[1] > tamanhoBorda):
        estaNaBordaSuperiorGolDir=True
        return True,estaNaBordaInferiorGolEsq
    else:
        estaNaBordaSuperior=False
        estaNaBordaInferior=False
        estaNaBordaSuperiorGolDir=False
        estaNaBordaSuperiorGolEsq=False
        estaNaBordaInferiorGolDir=False
        estaNaBordaInferiorGolEsq=False
        return False,estaNaBordaInferior,estaNaBordaSuperior,estaNaBordaInferiorGolEsq,estaNaBordaInferiorGolDir,estaNaBordaSuperiorGolDir,estaNaBordaSuperiorGolEsq

def estaNaArea(ponto, trocouCampo):
    if trocouCampo:
        if(ponto[1] > 45 and ponto[1] < 85 and ponto[0] < 28):
            return True
        else:
            return False
    else:
        if(ponto[1] > 45 and ponto[1] < 85 and ponto[0] > 145):
            return True
        else:
            return False

def estaComBola(RD, bola, trocouCampo, erro):
    if(distancia(RD, bola) < 3.5 + erro):
        return True
    else:
        return False