# -*- coding: utf-8 -*-
"""

Objetivo:      Funções de cada jogador do time, goleiro, zagueiro e atacante
Data:          26/Outubro/2017
Autor:         RED DRAGONS UFSCAR - Divisão de Controle e Estratégia
Membros:       Alexandre Dias Negretti
                Carlos Basali
                George Maneta
                Marcos Augusto Faglioni Junior 
                Natália dos Santos Andrade
                Vinicius Ancheschi Strini

"""

from verificaControle import *
import enviarInfo
from calculaControle import *
from AcoesControle import *
from controle import *
# KalmanFilterVelocity import *
import numpy as np
from math import *

"""
Função:  goleiro
Objetivo: Guia o robô de qualquer ponto do campo, até a area do gol, uma vez atingida area do gol, o robô rotacionará ao longo com 90 ou -90 graus e então irá
apenas para frente e para trás, posicionando-se no eixo y proporcional ao posicionamento da bola, ele também é capaz de se mover para retirar a bola de uma região
próxima ao gol quando a bola estiver com uma velocidade muito baixa.

Parametros de entrada:

    ## r_g ##  vetor com 6 posições, sendo:
    [0] - Coordenada X do robô; [1] - Coordenada Y do robô; [2] - angulo do robô; [3] - KP (constante de controle);
    [4] - velocidade máxima;    [5] - Função do robo (0-goleiro; 1-zagueiro; 2-atacante); [6] - Código do robô (0 -> @; 1 -> &; 2 -> $)

    ## bola ## vetor de 2 posições, sendo:
    [0] - Coordenada X da bola; [1] - Coordenada Y da bola

    ## ser ##  Porta serial (em caso de não haver comunicador conectado, passar 0)

    ## ambienteReal ## variavél booleana responsável por ativar a simulação se falsa ou ativar a comunicação serial se verdadeira

    ## duasFaces ## Variavel booleana responsável por ativar as duas frentes do robô

    ## trocouCampo ## Variavel booleana responsável por informar qual o lado do campo que está o jogo corrente

    ## debug ## Faz, em tempo de execução, exibir dados relevantes no terminal

    ## clientID ## Criado na main (caso Strini seja falso, fazer clientID = 0)

Retorno:

    ## angulo_d ## Valor na forma de float indicando o angulo desejado que o robô deverá atingir

Funções utilizadas:

    ## atingiuAlvo() ## Documentação disponivel em verificaControle.py
    
    ## dados_controle() ## Documentação disponivel em enviarInfo.py

    ## controle() ## Documentação disponivel em controle.py

"""

#FiltroBola = KalmanFilterVelocity(0.001,0.1)

#Variaveis para que um jogador tenha prioridade em ir para cima da bola em determinada situaçao
#flagDesviaG o zagueiro se asfastara da bola e com isso o goleiro ira retirar ela do gol
#flagDesviaZ o atacante se asfastara da bola e com isso o zagueiro ira retirar ela da faixa entre o meio do campo e o gol

flagDesviaG = False
flagDesviaZ = False
flagTrocouPosicao = False
def goleiro(r_g, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID):

    alvog=bola
    #print("Alvo:", alvog)
    angulo_d, flagInverteuTheta = controle(r_g, alvog, ser, ambienteReal, duasFaces, debug, clientID)
    '''
   #Raio da circunferencia
    r = 40
    #Distancia entre o ponto (10, 65) e a bola
    d = sqrt((bola[0] - 10)**2 + (bola[1] - 65)**2)
    #Distancia entre o ponto (160, 65) e a bola para o campo trocado
    d2 = sqrt((bola[0] - 160)**2 + (bola[1] - 65)**2)

    angulo_d = 0
    alvog = np.zeros([2])
    toleranciaRoboBola = 10
    
    #Velocidade da bola calculada pelo filtro de Kalman em X e Y
    #velBolaX, velBolaY = FiltroBola.update_states(bola[0],bola[1])
    
    #Módulo da velocidade da bola
    velMod = 1000 #sqrt((velBolaX)**2+(velBolaY)**2)
    
    #Flag para que o zagueiro saiba que o goleiro esta com a bola
    global flagDesviaG

    #Verifica se a bola esta dentro do semicirculo do gol e a velocidade da bola eh zero  
    if((d < r and velMod < 7.5 and (not trocouCampo)) or (d2 < r and velMod < 7.5 and trocouCampo)): 
        #Vai ate a bola, quando a bola entrar em movimento o goleiro retorna ao gol
        flagDesviaG = True
        alvog = seguirAlvo(bola)
        angulo_d ,flagInverteuTheta = controle(r_g, alvog, ser, ambienteReal, duasFaces, debug, clientID)

    else:
        #Estratégia Normal em que ele segue a bola em Y com angulo de 90°
        flagDesviaG = False
        if(trocouCampo):
            alvog = seguirEixoY(bola,155,[46,80])               
        else:
            alvog = seguirEixoY(bola,15,[46,80])
        #Verifica se o goleiro esta em frente a linha do gol
        if (not atingiuAlvo(r_g, bola, toleranciaRoboBola)):  
            #Verifica se o goleiro nao esta na bola                                
            if((r_g[0] > 15 and r_g[0] < 16 and (not trocouCampo)) or (r_g[0] > 155 and r_g[0] < 156 and trocouCampo)):
                #Verifica se o goleiro esta no alvo Y
                if(atingiuAlvoY(r_g, alvog, 3)):    
                    #Verificação em duas etapas afim de saber se o robô atingiu o angulo 90º ou -90º
                    if(not atingiuAngulo(r_g, math.pi/2, 0.17)):
    
                        if(not atingiuAngulo(r_g, -math.pi/2, 0.17)):    
                            #Caso ainda não tenha atingido, virar em torno do próprio eixo até obter o ângulo desejado
                            angulo_d,flagInverteuTheta = enviarInfo.dados_controle(r_g, ser, r_g[4]*0.1, r_g[4]*0.1, 0, 1, ambienteReal, debug, clientID)
    
                        else:
                            #Caso tenha atingido o ângulo -90º, paraS
                            angulo_d,flagInverteuTheta = enviarInfo.dados_controle(r_g, ser, 0, 0, 0, 0, ambienteReal, debug, clientID)                            
    
                    else:
                        #Caso tenha atingido o ângulo 90º, para
                        angulo_d,flagInverteuTheta = enviarInfo.dados_controle(r_g, ser, 0, 0, 0, 0, ambienteReal, debug, clientID)
    
                #Invoca o controle básico, com alvo na região demarcada
                else:
                    angulo_d ,flagInverteuTheta = controle(r_g, alvog, ser, ambienteReal, duasFaces, debug, clientID)
            #Se o goleiro não está sobre a linha do gol
            else:
                if(trocouCampo):
                    alvog[0] = 155
                else:
                    alvog[0] = 15
                angulo_d ,flagInverteuTheta = controle(r_g, alvog, ser, ambienteReal, duasFaces, debug, clientID)    
        #Se o goleiro esta na bola
        else:
            #Quando a bola chega nele, ele gira para o sentido em que a bola vá para o campo adversário
            #Se a bola está na parte de cima
            if(r_g[1] < 60):                    
                if(trocouCampo):
                    #Girar sentido anti-horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_g, ser, r_g[4]*2, r_g[4]*2, 1, 0, ambienteReal, debug, clientID)    
                else:
                    #Girar sentido horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_g, ser, r_g[4]*2, r_g[4]*2, 0, 1, ambienteReal, debug, clientID)
            #Se a bola está na parte de baixo
            elif(r_g[1] > 70):    
                if(trocouCampo):
                    #Girar no sentido horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_g, ser, r_g[4]*2, r_g[4]*2, 0, 1, ambienteReal, debug, clientID) 
                else:
                    #Girar no sentido anti-horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_g, ser, r_g[4]*2, r_g[4]*2, 1, 0, ambienteReal, debug, clientID)
            else:
                if(trocouCampo):
                    alvog = seguirEixoY(bola,155,[46,80])
                else:
                    alvog = seguirEixoY(bola,15,[46,80])
                angulo_d ,flagInverteuTheta = controle(r_g, alvog, ser, ambienteReal, duasFaces, debug, clientID)       
    '''            
    return angulo_d, flagInverteuTheta



"""
Função:  zagueiro
Objetivo: A estrategia escolhida do zagueiro foi ele possuir três comportamentos conforme a posição da bola: com uma posição em X maior
que que um valor r (menor que 170-r para trocou de campo), o zagueiro irá se pocionar em X com o valor de r (ou 170-r) e irá seguir a bola
em Y, caso a bola esteja dentro dessa area, mas fora de um circunferencia de raio r, o zagueiro irá em direção, caso a bola esteja dentro
da circunferencia o zagueiro irá traçar uma circunferencia em torno de um ponto específico ((10,65) jogando no lado normal ou (160,65)
jogando no lado invertido) de modo que ele fique entre a bola e este ponto, sem entrar na area do goleiro.
Ele também terá uma ação para caso a bola esteja muito lenta entre ele e o atacante.

Parametros de entrada:

    ## r_z ##  vetor com 6 posições, sendo:
    [0] - Coordenada X do robô; [1] - Coordenada Y do robô; [2] - angulo do robô; [3] - KP (constante de controle);
    [4] - velocidade máxima;    [5] - Função do robo (0-goleiro; 1-zagueiro; 2-atacante); [6] - Código do robô (0 -> @; 1 -> &; 2 -> $)

    ## bola ## vetor de 2 posições, sendo:
    [0] - Coordenada X da bola; [1] - Coordenada Y da bola

    ## ser ##  Porta serial (em caso de não haver comunicador conectado, passar 0)

    ## ambienteReal ## variavél booleana responsável por ativar a simulação se falsa ou ativar a comunicação serial se verdadeira

    ## duasFaces ## Variavel booleana responsável por ativar as duas frentes do robô

    ## trocouCampo ## Variavel booleana responsável por informar qual o lado do campo que está o jogo corrente

    ## debug ## Faz, em tempo de execução, exibir dados relevantes no terminal

    ## clientID ## Criado na main (caso Strini seja falso, fazer clientID = 0)

Retorno:

    ## angulo_d ## Valor na forma de float indicando o angulo desejado que o robô deverá atingir

Funções utilizadas:

    ## atingiuAlvo() ## Documentação disponivel em verificaControle.py
    
    ## dados_controle() ## Documentação disponivel em enviarInfo.py

    ## controle() ## Documentação disponivel em controle.py
"""

def zagueiro(r_z, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID):
    alvoz=bola
    angulo_d, flagInverteuTheta = controle(r_z, alvoz, ser, ambienteReal, duasFaces, debug, clientID)

    '''
    #Raio da circunferencia que o robo traçara
    r = 51

    #Criação do vetor que armazenará o alvo
    alvoz = np.zeros([2])

    #Distancia em centimetros que deve ser considerada para o robô estar com a bola
    toleranciaRoboBola = 8.5

    #Tolerancia usada para desviar o zagueiro do atacante
    toleranciaMeio = 7

    #Flags para desviar da bola
    global flagDesviaZ

    #Velocidade da bola calculada pelo filtro de Kalman em X e Y
    #velBolaX, velBolaY = FiltroBola.update_states(bola[0],bola[1])

    #Módulo da velocidade da bola
    velMod =1000 #sqrt((velBolaX)**2+(velBolaY)**2)

    #if principal, caso o robo não esteja na bola
    if(not atingiuAlvo(r_z, bola, toleranciaRoboBola)):

        #Caso trocouCampo seja verdadeiro, desenvolve a lógica para o lado contrário do campo e vice-versa
        if(trocouCampo):

            #Distancia entre o ponto (160, 65) e a bola
            d = sqrt((bola[0] - 160)**2 + (bola[1] - 65)**2)

            #Caso o zagueiro esteja no campo do adversário ele volta para o nosso campo
            #Isso é para a lógica de mudar de posição
            
            if(r_z[0] < 85):
                if(r_z[1]>= 65):
                    alvoz[0] = 110
                    alvoz[1] = bola[1] + 40
                else:
                    alvoz[0] = 110 
                    alvoz[1] = 2*bola[1] - 40

            #Verifica se a posição X da bola esta a frente da aréa em que o zagueiro irá de movimentar
            elif(bola[0] < (160-r)):
                alvoz = seguirEixoY(bola,160-r,[0,130])

                #Verifica se a bola esta lenta e entre o zagueiro e o atacante
                if(bola[0] > 95 and velMod < 7.5 and r_z[0] > 100):
                    flagDesviaZ = True
                    alvoz = seguirAlvo(bola)

            else:
                #Verifica se a bola e o zagueiro estão em hemisférios opostos do campo
                #Caso estejam o zagueiro irá para um ponto fixo, impedindo assim dele atravesar a área do gol
                flagDesviaZ = False
                if(r_z[1] < 65 and bola[1] >= 65):
                    alvoz[0] = (160-r)  
                    alvoz[1] = 70
                elif(r_z[1] > 65 and bola[1] <= 65):
                    alvoz[0] = (160-r)
                    alvoz[1] = 60
                else:
                    #Verifica se a bola esta fora da circunferencia de raio r e dentro da area de atuação do zagueiro
                    if(d > r):
                        alvoz = seguirAlvo(bola)

                    else:
                        alvoz = fazerSemicirculo(bola,[160,65],r)
                        if(flagDesviaG):
                            if(r_z[1]>=65):
                                alvoz[1]+=2*toleranciaMeio
                            else:
                                alvoz[1]-=2*toleranciaMeio

        #Lógica para quando não trocou de campo   
        else:
            #Distancia entre o ponto (10, 65) e a bola
            d = sqrt((bola[0] - 10)**2 + (bola[1] - 65)**2)

            #Caso o zagueiro esteja no campo do adversário ele volta para o nosso campo
            #Isso é para a lógica de mudar de posição

            if(r_z[0] > 85):
                if(r_z[1] >= 65):
                    alvoz[0] = 60
                    alvoz[1] = bola[1] + 40
                else:
                    alvoz[0] = 60
                    alvoz[1] = bola[1] - 40

            #Verifica se a posição X da bola esta a frente da aréa em que o zagueiro irá de movimentar
            elif(bola[0] > r):
                alvoz = seguirEixoY(bola,r,[0,130])

                #Verifica se a bola esta lenta e entre o zagueiro e o atacante
                if(bola[0] < 75 and velMod < 7.5 and r_z[0] < 70):
                    flagDesviaZ = True
                    alvoz = seguirAlvo(bola)

            else:
                #Verifica se a bola e o zagueiro estão em hemisférios opostos do campo
                #Caso estejam o zagueiro irá para um ponto fixo, impedindo assim dele atravesar a área do gol
                flagDesviaZ = False
                if(r_z[1] < 65 and bola[1] >= 65):
                    alvoz[0] = r  
                    alvoz[1] = 70
                elif(r_z[1] > 65 and bola[1] <= 65):
                    alvoz[0] = r
                    alvoz[1] = 60
                else:
                    # Verifica se a bola está pra fora da semicircunferência de raio r = 51
                    if(d > r):
                        alvoz = seguirAlvo(bola)

                    elif(d <= r):
                        alvoz = fazerSemicirculo(bola,[0,65],r)

        angulo_d, flagInverteuTheta = controle(r_z, alvoz, ser, ambienteReal, duasFaces, debug, clientID)

    #Caso o robo esteja na bola ele irá agir conforme a situação
    else:

        if(not trocouCampo):  

            if(r_z[1] > bola[1]):
            #Girar sentido horário
                angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_z, ser, r_z[4]*(50/22), r_z[4]*(50/22), 0, 1, ambienteReal, debug, clientID)
            else:
                #Girar sentido anti-horário
                angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_z, ser, r_z[4]*(50/22), r_z[4]*(50/22), 1, 0, ambienteReal, debug, clientID)
        else:

            if(r_z[1] > bola[1]):
                #Girar sentido anti-horário
                angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_z, ser, r_z[4]*(50/22), r_z[4]*(50/22), 1, 0, ambienteReal, debug, clientID)

            else:
                #Girar sentido horário
                angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_z, ser, r_z[4]*(50/22), r_z[4]*(50/22), 0, 1, ambienteReal, debug, clientID)

    '''            
    return angulo_d, flagInverteuTheta

"""
Função: Atacante
Objetivo: O atacante é programado para ir para um ponto atrás da bola, quando ele estiver neste ponto irá em direção a bola.
Quando o atacante estiver com a bola ele irá para o gol.

Parametros de entrada:

    ## r_a ##  vetor com 6 posições, sendo:
    [0] - Coordenada X do robô; [1] - Coordenada Y do robô; [2] - angulo do robô; [3] - KP (constante de controle);
    [4] - velocidade máxima;    [5] - Função do robo (0-goleiro; 1-zagueiro; 2-atacante); [6] - Código do robô (0 -> @; 1 -> &; 2 -> $)

    ## bola ## vetor de 2 posições, sendo:
    [0] - Coordenada X da bola; [1] - Coordenada Y da bola

    ## ser ##  Porta serial (em caso de não haver comunicador conectado, passar 0)

    ## ambienteReal ## variavél booleana responsável por ativar a simulação se falsa ou ativar a comunicação serial se verdadeira

    ## duasFaces ## Variavel booleana responsável por ativar as duas frentes do robô

    ## trocouCampo ## Variavel booleana responsável por informar qual o lado do campo que está o jogo corrente

    ## debug ## Faz, em tempo de execução, exibir dados relevantes no terminal

    ## clientID ## Criado na main (caso Strini seja falso, fazer clientID = 0)

Retorno:

    ## angulo_d ## Valor na forma de float indicando o angulo desejado que o robô deverá atingir

Funções utilizadas:

    ## atingiuAlvo() ## Documentação disponivel em auxiliarControle.py
    
    ## dados_controle() ## Documentação disponivel em controle.py

    ## controle() ## Documentação disponivel em controle.py
"""

#Flag para contar quando o atacante está preso na borda
Cont_Robo_Preso = 0

#Flag para armazenar a posição do atacante
Pos_anterior_robo = np.zeros([2])

def atacante(r_a, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID):

    alvoa=bola

    angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
    '''
    #vetor que armazena uma variação de cordenadas da bola no eixo y (-k*bola[0],+k*bola[0])
    dyb = 7 #constante para definir o intervalo de distancia lateral da bola
    dxb = 5 #constante para definir uma distância para o robô ir atrás da bola

    #Vetor que armazenará o alvo
    alvoa = np.zeros([2])

    #Vetor do ponto atrás da bola
    atrasBola = np.zeros([2])

    #Vetor que armazena as coordenadas do gol
    gol = np.zeros([2])
    
    #Vetor que armazena as coordenadas da área
    areaGol= np.zeros([2])
    #Angulo desejado
    angulo_d = 0

    #Variavel que indica se o angulo mudou (o angulo vai de 180 a -180 graus)
    flagInverteuTheta = False

    #Distancia em centimentros para considerar se o robo está na borda ou não
    tamanhoLateral = 15

    #Distancia em X atrás da bola onde há um ponto para onde o robo irá antes do chute
    distAtrasBola = 18  

    #Multiplicador da velocidade maxima usado no giro da lateral
    KgiroLateral = (50/30)

    #Tolerancia para o atacante não ficar no mesmo Y do zagueiro (impede que a bola fique rebatendo entre os dois)
    toleranciaMeio = 7

    #Distancia em centimetros que deve se considerar que o robo esteja no alvo
    ToleranciaDistRoboAlvo = 7

    #O gol para o atacante é o ponto do meio do gol real
    gol[1] = 65
    areaGol[1]=65

    if (trocouCampo):
        gol[0] = 0
        areaGol[0]=10
        #Caso troque o campo o "atras da bola" muda, pois muda a referencia (o gol)
        distAtrasBola = -distAtrasBola

    else:
        areaGol[0]=140
        gol[0] = 170

    #posição atrás da bola
    atrasBola[0] = bola[0] - distAtrasBola

    #Setando o alvo como o ponto atras da bola

    ########################################## verificar isso aqui VVVVVV
    
    if(r_a[1] > bola[1]):
        atrasBola[1] = bola[1] - distAtrasBola*0.4

    else:
        atrasBola[1] = bola[1] + distAtrasBola*0.4


    #distancia em Y do robo ate a bola
    dy = abs(r_a[1] - bola[1])

    #Utiliza-se somente o sinal da variavel dx para determinar se o robo está "atras da bola" (considerando a referencia certa)
    dx = (r_a[0] - bola[0])*distAtrasBola

    #calculo do angulo desejado
    delta_x = alvoa[0] - r_a[0]
    delta_y = alvoa[1] - r_a[1]
    angDesejado = np.arctan2(delta_y,delta_x)    

    #calculo do erro do angulo
    angErro = abs(angDesejado - r_a[2])
    
    global Cont_Robo_Preso
    global Pos_anterior_robo

    #Verificando se o robo está na lateral e a posição anterior é igual a posição atual
    if(((r_a[0] <= Pos_anterior_robo[0] + 1) and (r_a[0] >= Pos_anterior_robo[0] - 1)) and 
        ((r_a[1] < 10 or r_a[1] > 120) or (r_a[0] > 150 or r_a[0] < 20))):
        Cont_Robo_Preso += 1
    else:
        Cont_Robo_Preso = 0

    #Armazenando posição do robo na flag Pos_anterior_robo
    Pos_anterior_robo = r_a

    #Se a flag chegar a determinado valor, manda o robo dar ré
    if(Cont_Robo_Preso >= 2):
        if(r_a[1] > 110 or (r_a[0] > 150 and r_a[1] > 90)):             #Verifica se o robo está na parte de cima    
            alvoa[0] = r_a[0] - 7
            alvoa[1] = r_a[1] - 7
            Cont_Robo_Preso = 0
            angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

        elif(r_a[1] < 20 or (r_a[0] > 150 and r_a[1] < 40)):            #Verifica se o robo está na parte de baixo
            alvoa[0] = r_a[0] - 7
            alvoa[1] = r_a[1] + 7
            Cont_Robo_Preso = 0
            angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
        #Logica para campo invertido
        elif(r_a[0] < 20 and r_a[1] > 90):
            alvoa[0] = r_a[0] + 7
            alvoa[1] = r_a[1] - 7
            Cont_Robo_Preso = 0
            angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
        elif(r_a[0] < 20 and r_a[1] > 40):
            alvoa[0] = r_a[0] + 7
            alvoa[1] = r_a[1] + 7
            Cont_Robo_Preso = 0
            angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
        else:  #Caso o robo esteja preso com o goleiro inimigo, ele permanecerá preso
            Cont_Robo_Preso = 0

    else:
        #Verificando se o alvo do robô está nos limites do campo:
        #Verificação se a bola esta na defesa e o atacante está na frente da bola(o atacante não entra na defesa para não causar penaltis)
        if( (bola[0] < 75 and r_a[0] > bola[0]) and (not trocouCampo) ):

            #Verifica se o zagueiro esta indo pra bola
            if(bola[0] > 54 and flagDesviaZ):
                #No hemisfério superior do campo, ele desvia para cima da bola para não bater no zagueiro    
                if(bola[1] < 65):
                    alvoa[0] = 85
                    alvoa[1] = bola[1] + 2*toleranciaMeio

                #No hemisfério inferior do campo, ele desvia para baixo da bola para não bater no zagueiro
                else:  
                    alvoa[0] = 85
                    alvoa[1] = bola[1] - 2*toleranciaMeio

            else:
                if(bola[1] < 65):
                    alvoa[0] = 77
                    #A toleranciaMeio inpede que o atacante e o zagueiro fiquem na mesma linha de ação impendindo que o atacante rebata a bola diretamente para a defesa
                    alvoa[1] = bola[1] + 2*toleranciaMeio

                else:  
                    alvoa[0] = 77
                    alvoa[1] = bola[1] - 2*toleranciaMeio

            angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

        #Verificação se a bola esta na defesa com o campo trocado
        elif( (bola[0] > 95 and r_a[0] < bola[0]) and trocouCampo):

            #Verifica se o zagueiro esta indo pra bola
            if(bola[0] < 114 and flagDesviaZ):

                if(bola[1] < 65):
                    alvoa[0] = 85
                    alvoa[1] = bola[1] + 2*toleranciaMeio

                else:
                    alvoa[0] = 85
                    alvoa[1] = bola[1] - 2*toleranciaMeio

            else:   
                if(bola[1] < 65):
                    alvoa[0] = 93
                    alvoa[1] = bola[1] + 2*toleranciaMeio

                else:
                    alvoa[0] = 93
                    alvoa[1] = bola[1] - 2*toleranciaMeio

            angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

        #Nesse ponto sabemos que o X do robo é menor que o X da bola(O robo está atrás da bola)
        #Verificar se a bola está na lateral, para que o robo vá atrás da bola sem bater na lateral
        elif(bola[1] < 7 and (not atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo))):
            alvoa[1] = bola[1] + 3
            alvoa[0] = bola[0]
            angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
        #Se a bola está na lateral e o robo encosta nela, ele irá girar
        elif(bola[1] < 7 and (atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo))):
            angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 0, 1, ambienteReal, debug, clientID)
        #Verificação de bola na lateral superior do simulador
        elif(bola[1] > 123 and (not atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo))):
            alvoa[1] = bola[1] - 3
            alvoa[0] = bola[0]
            angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

        elif(bola[1] > 123 and (atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo))):
            angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 1, 0, ambienteReal, debug, clientID)
        
        #Os proximos 4 IF's são as verificações das 4 bordas do campo
        elif (estaNaBordaSuperior(r_a, tamanhoLateral)):
            #Verificação se o robo está na bola
            if(atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo)):
                #Bola esta na lateral superior
                if (trocouCampo):
                    #girar sentido anti-horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 1, 0, ambienteReal, debug, clientID)
                else:
                    #girar sentido horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 0, 1, ambienteReal, debug, clientID)

            #Verificação se a bola está na borda do gol
            elif(bola[0] > 157):
                alvoa[0] = bola[0] - 5
                alvoa[1] = bola[1]
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
            elif(bola[0] < 13):
                alvoa[0] = bola[0] + 5
                alvoa[1] = bola[1]
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

            #Se o robo não estiver na bola ele irá para a bola
            else:
                alvoa = bola
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
            
        #Segue a mesma lógica que há dentro do if anterior      
        elif(estaNaBordaInferior(r_a, tamanhoLateral)):

            if(atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo)):
                #bola está na lateral inferior
                if (trocouCampo):
                    #girar sentido horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 0, 1, ambienteReal, debug, clientID)
                else:
                    #girar sentido anti-horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 1, 0, ambienteReal, debug, clientID)

            #Verificação se a bola está na borda do gol
            elif(bola[0] > 157):
                alvoa[0] = bola[0] - 5
                alvoa[1] = bola[1]
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
            elif(bola[0] < 13):
                alvoa[0] = bola[0] + 5
                alvoa[1] = bola[1]
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
 
            else:
                alvoa = bola
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
            
        elif((estaNaBordaSuperiorGolDir(r_a, tamanhoLateral)) or (estaNaBordaSuperiorGolEsq(r_a, tamanhoLateral))):
            if(atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo)):
                #Bola esta na lateral superior
                if (trocouCampo):
                    #girar sentido anti-horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 1, 0, ambienteReal, debug, clientID)
                else:
                    #girar sentido horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 0, 1, ambienteReal, debug, clientID)
            #Se a bola estiver colada na borda e o robo nao estiver na bola, o robo ira um pouco abaixo da bola no eixo Y
            elif(bola[1] < 5):
                alvoa[0] = bola[0]
                alvoa[1] = bola[1] + 2
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

            #Se o robo não estiver na bola ele irá para a bola
            else:
                alvoa = bola
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
            
        #Segue a mesma lógica que há dentro do if anterior      
        elif(estaNaBordaInferior(r_a, tamanhoLateral)):

            if(atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo)):
                #bola está na lateral inferior
                if (trocouCampo):
                    #girar sentido horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 0, 1, ambienteReal, debug, clientID)
                else:
                    #girar sentido anti-horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 1, 0, ambienteReal, debug, clientID)
            
            #Se a bola estiver colada na borda e o robo nao estiver na bola, o robo ira um pouco acima da bola no eixo Y
            elif(bola[1] > 125):
                alvoa[0] = bola[0]
                alvoa[1] = bola[1] - 2
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

            else:
                alvoa = bola
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
            
        elif((estaNaBordaSuperiorGolDir(r_a, tamanhoLateral)) or (estaNaBordaSuperiorGolEsq(r_a, tamanhoLateral))): 
            if(atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo)):
                if (trocouCampo):
                    #girar sentido anti-horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 1, 0, ambienteReal, debug, clientID)
                else:
                    #girar sentido horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 0, 1, ambienteReal, debug, clientID)
            #Se a bola esta na borda do eixo X e o robo nao esta na borda, o robo vai um pouco atras da bola no eixo X
            elif(bola[0] < 13 and (estaNaBordaSuperiorGolEsq(r_a, tamanhoLateral))):
                alvoa[0] = bola[0] + 5
                alvoa[1] = bola[1]
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

            elif(bola[0] > 157 and (estaNaBordaSuperiorGolDir(r_a, tamanhoLateral))):
                alvoa[0] = bola[0] - 5
                alvoa[1] = bola[1]
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

            else:
                alvoa = bola
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)


        elif((estaNaBordaInferiorGolDir(r_a, tamanhoLateral)) or (estaNaBordaInferiorGolEsq(r_a, tamanhoLateral))):

            if(atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo)):
                if (not trocouCampo):
                    #girar sentido anti-horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 1, 0, ambienteReal, debug, clientID)
                else:
                    #girar sentido horário
                    angulo_d, flagInverteuTheta = enviarInfo.dados_controle(r_a, ser, r_a[4]*KgiroLateral, r_a[4]*KgiroLateral, 0, 1, ambienteReal, debug, clientID)
            
            #Se a bola esta na borda do eixo X e o robo nao esta na borda, o robo vai um pouco atras da bola no eixo X
            elif(bola[0] < 13 and (estaNaBordaInferiorGolEsq(r_a, tamanhoLateral))):
                alvoa[0] = bola[0] + 5
                alvoa[1] = bola[1]
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

            elif(bola[0] > 157 and (estaNaBordaInferiorGolDir(r_a, tamanhoLateral))):
                alvoa[0] = bola[0] - 5
                alvoa[1] = bola[1]
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

            else:
                alvoa = bola
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
           
           
        #Após a verificação das bordas, concluisse que o robo não esta em nenhuma borda
        else:         
            #Se o robo não esta em nenhuma borda, verifica se ele esta na bola
            if(atingiuAlvo(r_a, bola, ToleranciaDistRoboAlvo)):
                #Se o robo esta na bola ele irá para o area do gol 
                alvoa = areaGol
                angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
                #Se o robo esta na bola e na area do gol ele irá para o gol
                if(atingiuAlvo(r_a,areaGol,ToleranciaDistRoboAlvo)):
                    alvoa = gol
                    angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)

            #Se o robo não esta na bola
            else:
                #Verificação se o robo está no ponto atrás da bola
                if(dy < ToleranciaDistRoboAlvo and dx < 0 ):
                    #if(atingiuAngulo(r_a,0,0.37) or atingiuAngulo(r_a,- math.pi,0.37) or atingiuAngulo(r_a,math.pi,0.37)):
                    #Se o robo esta neste ponto, vá para a bola
                    alvoa = bola
                    angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
                    #else:
                        #angulo_d,flagInverteuTheta = dados_controle(r_a, ser, r_a[4]*0.28, r_a[4]*0.28, 0, 1, ambienteReal, debug, clientID)
                #Se o robo não esta no ponto, irá para o ponto atrás da bola
                else:
                    alvoa = atrasBola
                    angulo_d, flagInverteuTheta = controle(r_a, alvoa, ser, ambienteReal, duasFaces, debug, clientID)
    '''
    return angulo_d, flagInverteuTheta


def troca_posicao(r_a,r_z,bola,ser, ambienteReal, duasFaces, trocouCampo, debug, clientID):

    #Flag para saber a posição dos jogadores esta trocada
    global flagTrocouPosicao
    #Caso a bola esteja perto dos gols
    if(bola[0] < 50 or bola[0] >=100):
        if(flagTrocouPosicao):
            atacante(r_z, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
            zagueiro(r_a, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
        else:
            atacante(r_a, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
            zagueiro(r_z, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
    #Caso a bola esteja entre as cruzetas de cada time
    else:
        if(not flagTrocouPosicao):
            if(bola[0] < r_a[0]):             
                atacante(r_z, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
                zagueiro(r_a, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
                flagTrocouPosicao = True
            else:
                atacante(r_a, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
                zagueiro(r_z, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
                flagTrocouPosicao = False

        else:
            if(bola[0] < r_z[0]):
                atacante(r_a, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
                zagueiro(r_z, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
                flagTrocouPosicao = False
            else:
                atacante(r_z, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
                zagueiro(r_a, bola, ser, ambienteReal, duasFaces, trocouCampo, debug, clientID)
                flagTrocouPosicao = True
