import cv2
import numpy as np
import threading
from reddragons.visao import estruturas
from reddragons.visao import captura
import time
from reddragons.visao.logger import logger
import copy
import math

cam = captura.Imagem()

class processamento():
    def __init__(self, src="videos/jogo.avi"):
        self.Imagem = estruturas.estruturaImagem()
        self.Dados = estruturas.estruturaDados()
        self.DadosControle = estruturas.estruturaControle()
        self.started = False
        self.read_lock = threading.Lock()
        global cam
        cam.iniciar()
        
        self.recalcular()
        self.verbose = False
        

    def alterarSrc(self, src="videos/jogo.avi"):
        self.stop()
        global cam
        cam.alterarSrc(src)
        self.started = False
        self.iniciar()
        
    def mudarVerbose(self):
        self.verbose = not self.verbose
            
    def iniciar(self):
        if self.started:
            return None
        self.started = True
        self.thread = threading.Thread(target=self.processar, args=())
        self.thread.start()
        return self
        
    def processar(self):
        i_frame = 0
        while self.started:
            tempoInicial = time.time()
        
            global cam
            self.conseguiu, self.img = cam.read()
            
            if self.conseguiu:
                #self.img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                i_frame += 1
                tempoCamera = time.time()
                
                Imagem = copy.deepcopy(self.Imagem)
                Dados = copy.deepcopy(self.Dados)
                Imagem.imagem_original = copy.deepcopy(self.img)
                tempoCopia = time.time()
                
                _img = warpPerspective(Imagem.imagem_original, Dados)
                Imagem.imagem_warp = copy.deepcopy(_img)
                tempoWarp = time.time()
                
                _img2 = corteImagem(_img, Dados)
                Imagem.imagem_crop = copy.deepcopy(_img2)
                tempoCorte = time.time()
            
                Imagem.imagem_HSV = cv2.cvtColor(np.uint8(Imagem.imagem_crop), cv2.COLOR_RGB2HSV)
                tempoHSV = time.time()
                
                D = []
                for cor, filtro in zip(self.Dados.cores, self.Dados.filtros):
                    cortornos, hierarquia = getContornoCor(Imagem.imagem_HSV, cor, filtro)
                    centroids = np.empty((0, 3))
                    for c in cortornos:
                        M = cv2.moments(c)
                        if  ((M["m00"] >= self.Dados.AreaMinimo) and (M["m00"] <= self.Dados.AreaMaxima)):                
                            cX = int(M["m10"] / M["m00"])
                            cY = int(M["m01"] / M["m00"])
                            centroids = np.vstack(
                                (centroids, np.asarray([cX,cY,M["m00"]]))
                            )
                    D.append(np.array([centroids]))
                Imagem.centroids = D
                
                tempoCentroids = time.time()
                
                centros = calculaCentros(D, Dados.angCorr)
                
                    
                if self.Imagem.centros is not None:
                    if abs(centros[0][2] - self.Imagem.centros[0][2]) < 0.30:
                        centros[0][2] = centros[0][2] - (centros[0][2] - self.Imagem.centros[0][2])*0.85
                        
                    if abs(centros[1][2] - self.Imagem.centros[1][2]) < 0.30:
                        centros[1][2] = centros[1][2] - (centros[1][2] - self.Imagem.centros[1][2])*0.85
                        
                    if abs(centros[2][2] - self.Imagem.centros[2][2]) < 0.30:
                        centros[2][2] = centros[2][2] - (centros[2][2] - self.Imagem.centros[2][2])*0.85
                    
                Imagem.centros = centros
                
                adversarios = [[0, 0], [0, 0], [0, 0]]
                Imagem.adversarios = D[5]
                
                tempoCentros = time.time()
                    
                with self.read_lock:
                    self.Imagem = copy.deepcopy(Imagem)

                tempoFinal = time.time()
                
                if self.verbose:
                    logger().tempo(i_frame, tempoInicial, tempoCamera, tempoCopia, tempoWarp, tempoCorte, tempoHSV, tempoCentroids, tempoCentros, tempoFinal)                
            else:
                logger().erro('Sem frame da captura')
                cam.stop()
                cam = captura.Imagem()
                cam.iniciar()
                logger().flag('Câmera reiniciada')        
    
    def recalcular(self):
        Dados = self.Dados
        Dados.M_warpPerspective = matriz_warpPerspective(Dados)
        
        with self.read_lock:
            self.Dados = Dados
        
    def read_Imagem(self):
        with self.read_lock:
            Imagem = self.Imagem
        return Imagem
        
    def read_Dados(self):
        with self.read_lock:
            Dados = self.Dados
        return Dados
        
    def set_Dados(self, dados):
        with self.read_lock:
            self.Dados = dados

    def get_referencia(self):
        with self.read_lock:
            img = self.Imagem.imagem
        return img
        
    def stop(self):
        self.started = False
        self.thread.join()
        global cam
        cam.stop()

    def read_DadosControle(self):
        with self.read_lock:
            DadosControle = self.DadosControle
        return DadosControle

    def set_DadosControle(self,DadosControle):
        with self.read_lock:
            self.DadosControle = DadosControle

    def sincronizar_Controle(self):
        DadosControle = self.DadosControle
        Dados = self.Dados

        DadosControle.distCruzX = abs(Dados.cruzetas[0][0] - Dados.cruzetas[1][0])
        DadosControle.distCruzY = abs(Dados.cruzetas[0][1] - Dados.cruzetas[2][1])
        DadosControle.constX = 70.0/DadosControle.distCruzX
        DadosControle.constY = 37.5/DadosControle.distCruzY

        DadosControle = self.sincronizar_Controle_dinamico(DadosControle)
        self.set_DadosControle(DadosControle)
        return DadosControle
         

    def sincronizar_Controle_dinamico(self, DadosControle = None):
        if DadosControle is None:
             DadosControle = copy.deepcopy(self.DadosControle)
        Imagem = self.Imagem
        
        if Imagem.centroids[0] == []:
            logger().erro('Bola não detectada. Usando última posição')
        else:
            try:
                DadosControle.bola = (Imagem.centroids[0][0][0][0], Imagem.centroids[0][0][0][1])
            except:
                logger().erro(str(Imagem.centroids[0]))
                
        #logger().variavel('DadosControle.bola', DadosControle.bola)
        
        DadosControle.robot = Imagem.centros 
        #logger().variavel('DadosControle.robot', DadosControle.robot)
        err = self.checarErroCentroide(Imagem.centros)
        for i in range(3):
            if err[i] != 0:
                DadosControle.robot[i] = self.DadosControle.robot[i]
                logger().erro('Robô #' + str(i) + ' não detectado. Usando última posição')
        #logger().variavel('DadosControle.robot', DadosControle.robot)
        
        DadosControle.adversarios = Imagem.adversarios[0]
        #logger().variavel('DadosControle.adversarios', DadosControle.adversarios.T)
        
        self.set_DadosControle(DadosControle)
        
        return DadosControle
        
    def checarErroCentroide(self, centros):
        erros = [0, 0, 0]
        i = 0
        
        for c in centros:
            if c[0] == 0 or c[1] == 0:
                erros[i] += 1
                logger().erro('Um centro não detectado')
            i += 1
        return erros

    def __exit__(self, exec_type, exc_value, traceback):
        global cam
        cam.stop()
        
def corteImagem(fonte, estruturaDados):
    tamanho = estruturaDados.size
    
    imagem = fonte
    
    supEsquerdo = estruturaDados.corte[0]
    imagem[0:supEsquerdo[1], 0:supEsquerdo[0], :] = 0
    imagem[0:estruturaDados.corte[1][1], estruturaDados.corte[1][0]:640, :] = 0
    imagem[estruturaDados.corte[2][1]:480, 0:estruturaDados.corte[2][0], :] = 0
    imagem[estruturaDados.corte[3][1]:480, estruturaDados.corte[3][0]:640, :] = 0
    
    return imagem

def matriz_warpPerspective(estruturaDados):
    size = estruturaDados.size
    W = size[0]
    H = size[1]
    
    src = np.float32(estruturaDados.warpPerspective)
    dst = np.float32([[0,0], [W,0], [0,H], [W,H]])
    M = cv2.getPerspectiveTransform(src, dst)
    return M
    
def warpPerspective(imagem, estruturaDados):
    size = estruturaDados.size
    M = estruturaDados.M_warpPerspective
    
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
    
