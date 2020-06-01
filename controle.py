# -*- coding: utf-8 -*-
"""
@Data:			25/Outubro/2017
@Objetivo:		Função do controle básico do time do futebol de robôs da Universidade Federal de São Carlos - USFCar, e possui como objetivo ir até um alvo específico
@Autor:     	RED DRAGONS UFSCAR - Divisão controle e estratégia
@Membros:		Alexandre Dias Negretti
				Carlos Basali
				George Frisanco Maneta
				Marcos Augusto Faglioni Junior
				Natália dos Santos Andrade
				Vinicius Ancheschi Strini
"""
import math
from math import pi
import numpy as np
import random
#import cv2
import time
import enviarInfo
import estrategias

#Caso não exista os arquivos do V-rep, remover a importação do vrep, mas não será possível simular
#import vrep

erroAnterior = np.zeros(3)
somaErro = np.zeros(3)
tempoAtual = np.zeros(3)
tempoAnterior = np.zeros(3)
angulo_r_anterior = np.zeros(3)
velAngFiltrada = np.zeros(3)


constante_filtro_passa_baixa_velocidade_angular = 0.8,0.8,0.8

# Ganhos goleiro, zagueiro, atacante
KP = 0
KPang = KP,KP,KP
KIang = 0,0,0
KDang = 0,0,0

PWM_AnteriorR = 0
PWM_AnteriorL = 0

#Auxiliares para armazenar as velocidades em cada uma das rodas
rodaRpwm = 0
rodaLpwm = 0

sentidoR = 0
sentidoL = 0

pwmMaximoAEnviar = 1000
pwmMinimoAEnviar = 235
tempo=time.time()
#Variaveis de teste
ListaPWM = [350, 770, 420, 500, 810, 680, 900, 730, 850, 590]
numAmostras = 0
i = 0

"""
Função:	 Controle
Objetivo: Calcular a velocidade e sentido das rodas afim de guiaŕ o robô até o alvo dado; está função invoca o dados_controle para já enviar os dados para o robô, seja no simulador ou em ambiente real
Parametros de entrada:
	RD - vetor de 6 colunas, sendo:
        Colunas: 0 posição X; 1 posição Y; 2 angulo; 3 LP; 4 velocidade máxima; 5 função do robo (0-goleiro; 1-zagueiro; 3-atacante); 6 código do robô (0-@; 1-&; 2-!)
	alvo - Vetor de duas posição com as coordenadas (x,y) do alvo
	ser - Configurações da porta serial
	ambienteReal- variavél booleana responsável por ativar a simulação se verdadeira ou ativar a comunicação serial se falsa
	duasFaces - Variavel bolleana responsável por ativar as duas frentes do robô
    debug - Faz, em tempo de execução, exibir dados relevantes no terminal
    clientId - criado na main (caso simular seja falso, fazer clientID = 0)
Retorno:
    angulo_d - Variavel do tipo float, contendo o ângulo desejado
"""
def controle(RD, alvo, ser, ambienteReal, duasFaces, debug, clientID):
    #Decompondo o vetor RD em angulo_r, que é o ângulo do robô; pos_x_r e pos_y_r, que é respectivamente a posição x e y do robô ;
    angulo_r = RD[2]
    pos_x_r = RD[0]
    pos_y_r = RD[1]
    distanciaRodas = 4
    #global erroAnterior
    #global somaErro

    #Variáveis para o Filtro Passa Baixa
    #global PWM_AnteriorR
    #global PWM_AnteriorL
    #pesoNovaAcao = 0.7

    flagInverteuTheta = False
    indexRobo = int(RD[6])
    tempoAnterior[indexRobo] = tempoAtual[indexRobo]
    tempoAtual[indexRobo] = time.time()

    deltaTempo = tempoAtual[indexRobo] - tempoAnterior[indexRobo]
    deltaAngulo = angulo_r - angulo_r_anterior[indexRobo]
    angulo_r_anterior[indexRobo] = angulo_r
    # verificacao para evitar descontinuidades de angulo, entre -pi e pi, para isso o angulo
    # não deve variar mais de pi radianos entre um frame e outro

    if (deltaAngulo > pi):
        deltaAngulo -= 2*pi
    if (deltaAngulo < -pi):
        deltaAngulo += 2*pi

    ############### ESTIMATIVA DE VELOCIDADE ANGULAR #######

    velAngEstimada = deltaAngulo / deltaTempo

    ############### FILTRO PASSA BAIXA #####################

    constFiltro = constante_filtro_passa_baixa_velocidade_angular[indexRobo]
    velAngFiltrada[indexRobo]=(1-constFiltro)*velAngEstimada+constFiltro*velAngFiltrada[indexRobo]

    ############### LOG DE DADOS AQUI ######################
    #Arrumando o tempo
    if(indexRobo == 1):
        print(tempoAtual[indexRobo]-tempo)
        enviarInfo.infosLog(ListaPWM[i],angulo_r,velAngFiltrada[indexRobo],tempoAtual[indexRobo]-tempo);
        numAmostras += 1
        if(numAmostras == 40):
            numAmostras = 0
            i += 1
            if(i == 10):
                enviarInfo.criarLog()
                #Parar o código
                
    ###### Rotina para obtenção da relação PWM - Velocidade Angular de uma roda ######
 





    #informações do alvo
    pos_x_a = alvo[0]
    pos_y_a = alvo[1]
    #calculo do angulo desejado
    delta_x = pos_x_a - pos_x_r
    delta_y = pos_y_a - pos_y_r
    angulo_d = np.arctan2(delta_y,delta_x)

    #calculo da distancia absoluta do robo para o alvo
    distRA = math.sqrt((pos_x_r - pos_x_a)**2 + (pos_y_r - pos_y_a)**2)

    RaioRoda = 0.0345


    if (indexRobo == 0):
        print("\n GOLEIRO: ")
    if (indexRobo == 1):
        print("\n ZAGUEIRO: ")
    if (indexRobo == 2):
        print("\n ATACANTE: ")

    # print(">>> Robo numero: ",indexRobo, "  #goleiro=0,zagueiro=1,atacante=2")
    print("angulo_r :", 57.2958*angulo_r,"º; angulo_d :", 57.2958*angulo_d, "º; erro_angular :", 57.2958*angulo_e,"º")
    print("\n velocidade angular estimada(rad/s): ", velAngEstimada)
    print("Tempo Anterior: ", tempoAnterior[indexRobo])
    print("Tempo Atual: ", tempoAtual[indexRobo])
    print(" velocidade angular estimada(Hz): ", velAngEstimada*0.1591549, "\n")
    print("RODA R (rad/s): ", rodaR, "RODA R (pwm): ", rodaRpwm, "sentido: " , sentidoL)
    print("RODA L (rad/s): ", rodaL, "RODA L (pwm): ", rodaLpwm, "sentido: " , sentidoR)
    enviarInfo.dados_controle(RD, ser,ListaPWM[i],0, sentidoL, sentidoR, ambienteReal, debug, clientID)
    #PWM_AnteriorR = rodaRpwm
    #PWM_AnteriorL = rodaLpwm

    #Retorno do ângulo desejado para a visão poder exibir uma animação
    return angulo_d, flagInverteuTheta


