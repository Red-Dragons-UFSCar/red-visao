#Neste arquivo estão as funções responsáveis por transmitir ou salvar informações

# Import das bibliotecas utilizadas#
from datetime import datetime
import numpy as np
import pandas as pd
#import vrep
import serial 
from reddragons.controle import estrategias
import os
from reddragons.visao.estruturas import estruturaControle
from reddragons.controle import AcoesControle

def InicializaControle(Dados):
    DadosControle = estruturaControle()
    DadosControle = Dados

    if DadosControle.Pjogar:
        DadosControle.angulo_d,DadosControle.flagInverteuTheta = \
        dados_robo(DadosControle.robot,DadosControle.bola,
                   DadosControle.ser,DadosControle.constX,DadosControle.constY,
                   True,DadosControle.duasFaces,DadosControle.trocouCampo,
                   DadosControle.debug,DadosControle.clientID)

    elif DadosControle.Pparar:
        AcoesControle.parada(DadosControle.robot,DadosControle.bola,
                            DadosControle.ser,DadosControle.constX,
                            DadosControle.constX,DadosControle.constY,
                            True,DadosControle.duasFaces,
                            DadosControle.trocouCampo,DadosControle.debug,
                            DadosControle.clientID)

    elif DadosControle.Pinicial:
        AcoesControle.posicaoInicial(DadosControle.robot,DadosControle.bola,
                                     DadosControle.ser,DadosControle.constX,DadosControle.constY,
                                     True,DadosControle.duasFaces,DadosControle.trocouCampo,
                                     DadosControle.bolaNossa1,DadosControle.debug,DadosControle.clientID)

    
    return DadosControle


lista_log=[] #Criação de lista para o log de dados
#Função que adiciona um vetor de dados à lista, mais dados podem ser adicionados maualmente aumentando o número de variaveis na função
#As variaveis ficarão cada uma em uma coluna
def infosLog(var1,var2,var3,var4): 
    lista_log.append([var1,var2,var3,var4]) 
#Cria um arquivo csv com a lista de dados, o arquivo tem o nome com a data e tempo atual e é salvo na pasta logs
def criarLog():
    auxnome= datetime.now()
    nomearquivo=auxnome.strftime('%Y%m%d%H%M%S')
    df = pd.DataFrame(lista_log,columns=['Var 1','Var 2','Var3','Var 4'])
    df.to_csv('logs/'+nomearquivo+'.csv')
"""
Função:  serialEscreverPorta
Objetivo: Caso seja encaminhado um comando para a porta serial, e este possa ser executado, essa função encaminhará o código para a porta serial
    ser - Configurações da porta serial
    comando - Dado de formato string que contém o dado a ser enviado
    ambienteReal - Variável bolleana que libera ou não a escrita na porta serial
Retorno:
    Sem retorno
"""
def serialEscreverPorta(ser, comando, ambienteReal):
    if ambienteReal:
        if (ser.isOpen()):
            #Realiza a tentativa de envio de dados
            try:
                #print("entrouNo serial escrever porta")
                ser.flushInput()
                ser.flushOutput()
                ser.write(comando.encode())

            #Em caso de exception, exibe o erro
            except Exception as e:
                print("ERRO: " + str(e))


"""
Função:  dados_controle
Objetivo: Enviar dados via serial (se simular for falso) ou para o simulador V-rep (se simular for verdadeiro) de informações diretas, que não necessitam de tratamento algum
Parametros de entrada:
    RD - vetor de 6 colunas, sendo:
        Colunas: 0 posição X; 1 posição Y; 2 angulo; 3 KP; 4 velocidade máxima; 5 função do robo (0-goleiro; 1-zagueiro; 3-atacante); 6 código do robô (0-@; 1-&; 2-!)
    ser - Configurações da porta serial
    rodaL - Velocidade da roda esquerda
    rodaR - Velocidade da roda direita
    sentidoL - Sentido da roda esquerda (1 para frente e 0 para trás)
    sentidoR - Sentido da roda direita (1 para frente e 0 para trás)
    ambienteReal- variavél booleana responsável por ativar a simulação se verdadeira ou ativar a comunicação serial se falsa
    clientID - parâmetro necessário para o funcionamento do v-rep, criado na main (caso simular seja falso, fazer clientID = 0)
    debug - Faz, em tempo de execução, exibir dados relevantes no terminal
Retorno:
    Sem retorno
"""
def dados_controle(RD, ser, rodaL, rodaR, sentidoL, sentidoR, ambienteReal, debug, clientID):

    #Caso o Xbee esteja conectado, o comando será construido e encaminhado para a porta serial    
    if ambienteReal:
        #Construção do comando no formato em que a eletrônica aceita (formato código_do_robô)
        comandorobo1 = "%d,%.4d,%d,%.4d" % (sentidoL, rodaL, sentidoR, rodaR)
        
        #Determina qual robô receberá o comando
        if (RD[6] == 0):
            serialEscreverPorta(ser, '@' + comandorobo1 + '#', ambienteReal)
            #if debug:
            #print('Goleiro: ',ser, '@' + comandorobo1 + '#', ambienteReal)
        if (RD[6] == 1):
            serialEscreverPorta(ser, '&' + comandorobo1 + '#', ambienteReal)
            #if debug:
            #print('Zagueiro: ',ser, '&' + comandorobo1 + '#', ambienteReal)
        if (RD[6] == 2):
            serialEscreverPorta(ser, '!' + comandorobo1 + '#', ambienteReal)
            #if debug:
            #print('Atacante: ',ser, '!' + comandorobo1 + '#', ambienteReal)

    #Caso o Xbee não esteja conectado e se deseja utilizar o V-rep para simular
    if not ambienteReal:
        #Definição dos parâmetros necessários para o envio da informação para o V-rep
        if (RD[6] == 0):
            errorCode,left_motor_handle = vrep.simxGetObjectHandle(clientID,'MotorEsquerdoRobo1',vrep.simx_opmode_blocking)
            if debug:
                if errorCode == 0:
                    print("Sem erro")
                else:
                    print("Erro na criação do parametro para o MotorEsquerdoRobo1: %d" % errorCode)

            errorCode,right_motor_handle = vrep.simxGetObjectHandle(clientID,'MotorDireitoRobo1',vrep.simx_opmode_blocking)
            if debug:
                if errorCode == 0:
                    print("Sem erro")
                else:
                    print("Erro na criação do parametro para o MotorDireitoRobo1: %d" % errorCode)

        if (RD[6] == 1):
            errorCode,left_motor_handle = vrep.simxGetObjectHandle(clientID,'MotorEsquerdoRobo2',vrep.simx_opmode_blocking)
            if debug:
                if errorCode == 0:
                    print("Sem erro")
                else:
                    print("Erro na criação do parametro para o MotorEsquerdoRobo2: %d" % errorCode)

            errorCode,right_motor_handle = vrep.simxGetObjectHandle(clientID,'MotorDireitoRobo2',vrep.simx_opmode_blocking)
            if debug:
                if errorCode == 0:
                    print("Sem erro")
                else:
                    print("Erro na criação do parametro para o MotorDireitoRobo2: %d" % errorCode)

        if (RD[6] == 2):
            errorCode,left_motor_handle = vrep.simxGetObjectHandle(clientID,'MotorEsquerdoRobo3',vrep.simx_opmode_blocking)
            if debug:
                if errorCode == 0:
                    print("Sem erro")
                else:
                    print("Erro na criação do parametro para o MotorEsquerdoRobo3: %d" % errorCode)

            errorCode,right_motor_handle = vrep.simxGetObjectHandle(clientID,'MotorDireitoRobo3',vrep.simx_opmode_blocking)
            if debug:
                if errorCode == 0:
                    print("Sem erro")
                else:
                    print("Erro na criação do parametro para o MotorDireitoRobo3: %d" % errorCode)

        #O V-rep aceita valores negativos para as rodas, portanto, retorna-se o sentido como sendo o sinal da velocidade
        if sentidoL == 0:
            rodaL = -rodaL
        
        if sentidoR == 0:
            rodaR = -rodaR

        #Envio do código para o V-rep
        errorCode = vrep.simxSetJointTargetVelocity(clientID,left_motor_handle,rodaL,vrep.simx_opmode_streaming)
        if debug:
            if errorCode == 0:
                print("Sem erro")
            else:
                print("Erro ao enviar comando para o motor esquerdo: %d" % errorCode)
            
        errorCode = vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,rodaR,vrep.simx_opmode_streaming)
        if debug:
            if errorCode == 0:
                print("Sem erro")
            else:
                print("Erro ao enviar comando para o motor direito: %d" % errorCode)

    return 0,0


"""
Função:  dados_robo
Objetivo: A função dados robô recebe as coordenadas e os angulos dos robos e em cada linha da matriz inseri outros dados necessários para o controle do robô, como
o Kp de cada robô, a velocidade máxima de cada robô e o número da função de cada robô.

Parametros de entrada:

    ## RD ##  matriz 3x3, sendo:
    [0,X] - Coordenada X do robô; [1,X] - Coordenada Y do robô; [2,X] - angulo do robô

    ## bola ## vetor de 2 posições, sendo:
    [0] - Coordenada X da bola; [1] - Coordenada Y da bola

    ## ser ##  Porta serial (em caso de não haver comunicador conectado, passar 0)

    ## constX e constY ## Constantes para transformar pixels em metros

   	##ambienteReal- variavél booleana responsável por ativar a simulação se verdadeira ou ativar a comunicação serial se falsa

    ## duasFaces ## Variavel booleana responsável por ativar as duas frentes do robô

    ## trocouCampo ## Variavel booleana responsável por informar qual o lado do campo que está o jogo corrente

    ## debug ## Faz, em tempo de execução, exibir dados relevantes no terminal

    ## clientID ## Criado na main (caso simular seja falso, fazer clientID = 0)

Retorno:

    ## angulo_d ## Valor na forma de float indicando o angulo desejado que o robô deverá atingir

    ## flagInverteuTheta ## Variável booleana para identificar a mudança da referência do ângulo

"""

def dados_robo(RD, bola, ser, constX, constY,ambienteReal, duasFaces, trocouCampo, debug, clientID):

    #Criando a matriz para armazenar os dados extras de Kp, velocidade máxima, função do robo e código do robô
    dadosR = np.zeros([3, 7])

    #Criando o vetor para armazenar os ângulos desejados
    angulo_d = np.zeros([3])
    flagInverteuTheta = np.zeros([3])

    alvo = np.zeros([2])
    adv = False
    bola = list(bola)

    #0 posição X; 1 posição Y; 2 angulo; 3 KP; 4 velocidade máxima; 5 função do robo (0-goleiro; 1-zagueiro; 2-atacante); 6 código do robô (0-@; 1-&; 2-!)
    if (not ambienteReal):
        dadosR[0] = RD[0,0] * constX, RD[0,1] * constY, RD[0,2], 1, 12, 0, 0
        dadosR[1] = RD[1,0] * constX, RD[1,1] * constY, RD[1,2], 1, 12, 1, 1
        dadosR[2] = RD[2,0] * constX, RD[2,1] * constY, RD[2,2], 1, 12, 2, 2
    else:
        dadosR[0] = RD[0,0] * constX, RD[0,1] * constY, RD[0,2], 18, 1000, 0, 0
        dadosR[1] = RD[1,0] * constX, RD[1,1] * constY, RD[1,2], 18, 1000, 1, 1
        dadosR[2] = RD[2,0] * constX, RD[2,1] * constY, RD[2,2], 20, 1000, 2, 2
    # If para armazenar as posições do adversário caso a variavel adv seja True
    if(adv):
        dadosAD = np.zeros([3, 3])
        AD = np.zeros([3, 3])
        dadosAD[0] = AD[0,0] * constX, AD[0,1] * constY, AD[0,2]
        dadosAD[1] = AD[1,0] * constX, AD[1,1] * constY, AD[1,2]
        dadosAD[2] = AD[2,0] * constX, AD[2,1] * constY, AD[2,2]

    bola[0] = bola[0] * constX
    bola[1] = bola[1] * constY
    #print("Goleiro",dadosR[0])
    #print("Zagueiro",dadosR[1])
    #print("Atacante",dadosR[2])
    #print("entro nos dados do robo")

    duasFaces=False

    angulo_d[0], flagInverteuTheta[0] = estrategias.goleiro(dadosR[0], bola, ser,ambienteReal, duasFaces, trocouCampo, debug, clientID)

    angulo_d[1], flagInverteuTheta[1] = estrategias.zagueiro(dadosR[1], bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)

    angulo_d[2], flagInverteuTheta[2] = estrategias.atacante(dadosR[2], bola, ser,ambienteReal, duasFaces, trocouCampo, debug, clientID)

    #estrategias.troca_posicao(dadosR[2],dadosR[1], bola, ser, ambienteReal, False, trocouCampo, debug, clientID)


    return angulo_d, flagInverteuTheta
