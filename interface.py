from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from enum import Enum

import cv2
import numpy as np

import enviarInfo
from estruturas import *
from logger import *
import captura
import processamento
import serial

import sys
import pickle
import math

import glob, os

class Estado(Enum):
    ORIGINAL = 0
    PERSPECTIVA = 1
    CORTE = 2
    CRUZ = 3
    CENTROIDS = 4
    ROBOS = 5

VISAO = processamento.processamento()

class GUI_main(QMainWindow):
    def __init__(self):
    
        super(GUI_main, self).__init__()
        loadUi('interface/main.ui', self)
        
        self.QT_btVisualizacao.clicked.connect(self.visualizacao)
        self.QT_btPerspectiva.clicked.connect(self.perspectiva)
        self.QT_btCorte.clicked.connect(self.corte)
        self.QT_btCruzetas.clicked.connect(self.cruzetas)
        self.QT_btCores.clicked.connect(self.cores)
        self.QT_Load.clicked.connect(self.carregar)
        self.QT_Save.clicked.connect(self.salvar)
        self.QT_Centro.clicked.connect(self.centro)
        self.QT_FPS.clicked.connect(self.mudarVerbose)
        self.QT_Versao.clicked.connect(self.versao)
        self.QT_camera.clicked.connect(self.setCamera)
        self.QT_btcontrole.clicked.connect(self.controle)
        self.QT_jogo.clicked.connect(self.jogar)
        self.show()
        
        global VISAO
        VISAO.iniciar()
        
    def setCamera(self):
        self.tela = GUI_camera()
        
    def visualizacao(self):
        self.tela = GUI_visualizacao()
        
    def perspectiva(self):
        self.tela = GUI_perspectiva()
        
    def corte(self):
        self.tela = GUI_corte()
        
    def cruzetas(self):
        self.tela = GUI_cruzetas()
        
    def cores(self):
        self.tela = GUI_cores()
        
    def centro(self):
        self.tela = GUI_centro()

    def controle(self):
        self.tela = GUI_controle()

    def jogar(self):
        self.tela = GUI_jogar()

    def versao(self):
        logger().dado(cv2.getBuildInformation())
        
    def closeEvent(self, event):
        VISAO.stop()
        
    def mudarVerbose(self):
        VISAO.mudarVerbose()
        
    def salvar(self):
        self.tela = GUI_salvar()
    
    def carregar(self):
        self.tela = GUI_carregar()
        
class GUI_visualizacao(QMainWindow):
    def __init__(self):
        super(GUI_visualizacao, self).__init__()
        loadUi('interface/visualizacao.ui', self)
        self.show()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1)
        
    def closeEvent(self, event):
    	self.timer.stop()
    	event.accept()
        
    def updateFrame(self):
        estado = self.qt_tipoVisualizacao.currentIndex()
        
        global VISAO
        Imagem = VISAO.read_Imagem()
        Dados = VISAO.read_Dados()
        
        if estado == Estado.ORIGINAL.value:
            img = Imagem.imagem_original
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.PERSPECTIVA.value:
            img = Imagem.imagem_warp
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.CORTE.value:
            img = Imagem.imagem_crop
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.CRUZ.value:
            img = Imagem.imagem_crop
            for ponto in Dados.cruzetas:
                cv2.drawMarker(img, (ponto[0], ponto[1]), (255,0,0))
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.CENTROIDS.value:
            img = Imagem.imagem_crop
            C = [(55, 55, 55), (200, 200, 200), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
            for c, p in zip(C, Imagem.centroids):
                for _p in p[0]:
                    cv2.circle(img, (int(_p[0]), int(_p[1])), 8, c, -1)
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
            
        if estado == Estado.ROBOS.value:
            img = Imagem.imagem_crop
            C = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
            for c, p in zip(C, Imagem.centros):
                cv2.circle(img, (int(p[0]), int(p[1])), 25, c, 1)
                cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(p[2])*50), int(p[1]+ math.sin(p[2])*50)), c, 3)
                cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(Dados.angCorr)*50), int(p[1]+ math.sin(Dados.angCorr)*50)), c, 1)
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_visualizacao.setPixmap(_qPixmap)
        
class GUI_perspectiva(QMainWindow):
    def __init__(self):
        super(GUI_perspectiva, self).__init__()
        loadUi('interface/perspectiva.ui', self)
        self.show()    
        global VISAO
        self.dados = VISAO.read_Dados()
        
        self.getReferencia()
        
        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)
        
    def getReferencia(self):
        global VISAO
        self.referencia = VISAO.read_Imagem().imagem_original
        self.desenhar()
        
    def finalizar(self):
        global VISAO
        VISAO.set_Dados(self.dados)
        VISAO.recalcular()
        
    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()
        
        if (x < self.QT_Imagem.geometry().width()) and (y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0):
            self.dados.warpPerspective[self.QT_posicao.currentIndex()] = [x, y]
            self.desenhar()
            
    def desenhar(self):
        img = self.referencia.copy()
            
        pts = self.dados.warpPerspective
        pts = np.asarray([pts[0], pts[1], pts[3], pts[2]])
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,0),2)
        
        for ponto in self.dados.warpPerspective:
            cv2.circle(img, (ponto[0], ponto[1]), 6, (205,0,0),-1)
            
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Imagem.setPixmap(_qPixmap)

class GUI_corte(QMainWindow):
    def __init__(self):
        super(GUI_corte, self).__init__()
        loadUi('interface/corte.ui', self)
        self.show()    
        global VISAO
        self.dados = VISAO.read_Dados()
        
        self.getReferencia()
        
        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)
        
    def getReferencia(self):
        global VISAO
        self.referencia = VISAO.read_Imagem().imagem_warp
        self.desenhar()
        
    def finalizar(self):
        global VISAO
        VISAO.set_Dados(self.dados)
        VISAO.recalcular()
        
    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()
        
        if (x < self.QT_Imagem.geometry().width()) and (y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0):
            self.dados.corte[self.QT_posicao.currentIndex()] = [x, y]
            self.desenhar()
            
    def desenhar(self):
        img = self.referencia.copy()
        
        for ponto in self.dados.corte:
            cv2.drawMarker(img, (ponto[0], ponto[1]), (0,255,0))
            
        img[0:self.dados.corte[0][1], 0:self.dados.corte[0][0], :] = 0
        img[0:self.dados.corte[1][1], self.dados.corte[1][0]:640, :] = 0
        img[self.dados.corte[2][1]:480, 0:self.dados.corte[2][0], :] = 0
        img[self.dados.corte[3][1]:480, self.dados.corte[3][0]:640, :] = 0
            
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Imagem.setPixmap(_qPixmap) 

class GUI_cruzetas(QMainWindow):
    def    __init__(self):
        super(GUI_cruzetas, self).__init__()
        loadUi('interface/cruzetas.ui', self)
        self.show()
        global VISAO
        self.dados = VISAO.read_Dados()
        self.getReferencia()
        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_btFinalizar.clicked.connect(self.finalizar)
        
    def getReferencia(self):
        global VISAO
        self.referencia = VISAO.read_Imagem().imagem_warp
        self.desenhar()
        
    def finalizar(self):
        global VISAO
        VISAO.set_Dados(self.dados)
    
    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()
        
        if (x < self.QT_Imagem.geometry().width()) and (y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0):
            self.dados.cruzetas[self.QT_posicao.currentIndex()] = [x, y]
            self.desenhar()
            
    def desenhar(self):
        img = self.referencia.copy()
        
        for ponto in self.dados.cruzetas:
            cv2.drawMarker(img, (ponto[0], ponto[1]), (255,0,0))
            
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Imagem.setPixmap(_qPixmap) 

class GUI_cores(QMainWindow):
    def    __init__(self):
        super(GUI_cores, self).__init__()
        loadUi('interface/cores.ui', self)
        self.show()
        
        self.centroids = np.empty([0,3])
        
        global VISAO
        self.dados = VISAO.read_Dados()
        
        self.QT_AreaMax.setValue(self.dados.AreaMaxima)
        self.QT_AreaMin.setValue(self.dados.AreaMinimo)
        
        self.getReferencia()
        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_btSalvar.clicked.connect(self.salvar)
        self.QT_HMin.sliderMoved.connect(self.mudanca)
        self.QT_HMax.sliderMoved.connect(self.mudanca)
        self.QT_SMin.sliderMoved.connect(self.mudanca)
        self.QT_SMax.sliderMoved.connect(self.mudanca)
        self.QT_VMin.sliderMoved.connect(self.mudanca)
        self.QT_VMax.sliderMoved.connect(self.mudanca)
        self.QT_valorKernel.sliderMoved.connect(self.mudanca)
        self.QT_qualKernel.currentIndexChanged.connect(self.mudanca)
        self.QT_tipoKernel.currentIndexChanged.connect(self.mudanca)
        self.QT_AreaMax.sliderMoved.connect(self.mudanca)
        self.QT_AreaMin.sliderMoved.connect(self.mudanca)
        self.QT_selecao.currentIndexChanged.connect(self.novaCor)
        self.QT_fatorClique.sliderMoved.connect(self.fatorFiltro)
        self.QT_fatorCor.sliderMoved.connect(self.fatorFiltro)
        
        self.fatorFiltro()
        
        self.setMouseTracking(True)
        
        self.mask = None
        self.novaCor()
        
    def getReferencia(self):
        global VISAO
        self.referencia = VISAO.read_Imagem().imagem_crop
        self.imagem_HSV = VISAO.read_Imagem().imagem_HSV
        self.dados = VISAO.read_Dados()
        self.contornos, _ = processamento.getContornoCor(self.imagem_HSV, self.dados.cores[0], self.dados.filtros[0])
        self.desenhar()
        
    def salvar(self):
        i = self.QT_selecao.currentIndex()
        self.dados.cores[i] = [ [self.QT_HMin.value(), self.QT_SMin.value(), self.QT_VMin.value()], [self.QT_HMax.value(), self.QT_SMax.value(), self.QT_VMax.value()]]
        self.dados.filtros[i] = [ int(self.QT_qualKernel.currentIndex()), int(self.QT_tipoKernel.currentIndex()), self.QT_valorKernel.value()]
        
        self.dados.AreaMinimo = self.QT_AreaMin.value()
        self.dados.AreaMaxima = self.QT_AreaMax.value()
        global VISAO
        VISAO.set_Dados(self.dados)
        
    def novaCor(self):
        i = self.QT_selecao.currentIndex()
        self.contornos, _ = processamento.getContornoCor(self.imagem_HSV,  self.dados.cores[i], self.dados.filtros[i])
        
        cores = self.dados.cores[i]
        filtros = self.dados.filtros[i]
        
        self.QT_HMin.setValue(cores[0][0])
        self.QT_HMax.setValue(cores[1][0])
        
        self.QT_SMin.setValue(cores[0][1])
        self.QT_SMax.setValue(cores[1][1])
        
        self.QT_VMin.setValue(cores[0][2])
        self.QT_VMax.setValue(cores[1][2])
        
        self.QT_qualKernel.setCurrentIndex(filtros[0])
        self.QT_valorKernel.setValue(filtros[2])
        self.QT_tipoKernel.setCurrentIndex(filtros[1])
        
        
        self.desenhar()
        
    def fatorFiltro(self):
        self.fator_clique = self.QT_fatorClique.value()
        self.fator_cor = self.QT_fatorCor.value()
    
    def mudanca(self):
        i = self.QT_selecao.currentIndex()
    
        self.dados.cores[i] = [ [self.QT_HMin.value(), self.QT_SMin.value(), self.QT_VMin.value()], [self.QT_HMax.value(), self.QT_SMax.value(), self.QT_VMax.value()]]
        self.dados.filtros[i] = [ int(self.QT_qualKernel.currentIndex()), int(self.QT_tipoKernel.currentIndex()), self.QT_valorKernel.value()]
        
        self.contornos, _ = processamento.getContornoCor(cv2.cvtColor(np.uint8(self.referencia), cv2.COLOR_RGB2HSV),  self.dados.cores[i], self.dados.filtros[i])
        
        
        self.centroids = np.empty([0,3])
        for c in self.contornos:
            M = cv2.moments(c)
            if  ((M["m00"] >= self.QT_AreaMin.value()) and (M["m00"] <= self.QT_AreaMax.value())):                
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                self.centroids = np.append(self.centroids,[[cX,cY,M["m00"]]], axis = 0)
        
        self.desenhar()        
    
    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()
        
        if (x < self.QT_Imagem.geometry().width()) and (y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0):
            #logger().variavel("Cor no ponto ({0}, {1})".format(x,y), "RGB {0} HSV {1}".format(self.referencia[y, x], self.imagem_HSV[y, x]))
            if y > self.fator_clique and x > self.fator_clique and x < 640 - self.fator_clique and y < 480 - self.fator_clique:
                HMax = max(
                        self.imagem_HSV[y,x-self.fator_clique][0], 
                        self.imagem_HSV[y-self.fator_clique,x][0], 
                        self.imagem_HSV[y,x][0], 
                        self.imagem_HSV[y,x+self.fator_clique][0], 
                        self.imagem_HSV[y+self.fator_clique,x][0]
                )
                HMin = min(
                        self.imagem_HSV[y,x-self.fator_clique][0], 
                        self.imagem_HSV[y-self.fator_clique,x][0], 
                        self.imagem_HSV[y,x][0], 
                        self.imagem_HSV[y,x+self.fator_clique][0], 
                        self.imagem_HSV[y+self.fator_clique,x][0]
                )
                self.QT_HMin.setValue(max(0, HMin-self.fator_cor))
                self.QT_HMax.setValue(min(179, HMax+self.fator_cor))
                
                SMax = max(
                        self.imagem_HSV[y,x-self.fator_clique][1], 
                        self.imagem_HSV[y-self.fator_clique,x][1], 
                        self.imagem_HSV[y,x][1], 
                        self.imagem_HSV[y,x+self.fator_clique][1], 
                        self.imagem_HSV[y+self.fator_clique,x][1]
                )
                SMin = min(
                        self.imagem_HSV[y,x-self.fator_clique][1], 
                        self.imagem_HSV[y-self.fator_clique,x][1], 
                        self.imagem_HSV[y,x][1], 
                        self.imagem_HSV[y,x+self.fator_clique][1], 
                        self.imagem_HSV[y+self.fator_clique,x][1]
                )
                self.QT_SMin.setValue(max(0, SMin-self.fator_cor))
                self.QT_SMax.setValue(min(255, SMax+self.fator_cor))
                
                VMax = max(
                        self.imagem_HSV[y,x-self.fator_clique][2], 
                        self.imagem_HSV[y-self.fator_clique,x][2], 
                        self.imagem_HSV[y,x][2], 
                        self.imagem_HSV[y,x+self.fator_clique][2], 
                        self.imagem_HSV[y+self.fator_clique,x][2]
                )
                VMin = min(
                        self.imagem_HSV[y,x-self.fator_clique][2], 
                        self.imagem_HSV[y-self.fator_clique,x][2], 
                        self.imagem_HSV[y,x][2], 
                        self.imagem_HSV[y,x+self.fator_clique][2], 
                        self.imagem_HSV[y+self.fator_clique,x][2]
                )
                self.QT_VMin.setValue(max(0, VMin-self.fator_cor))
                self.QT_VMax.setValue(min(255, VMax+self.fator_cor))
            else:
                H, S, V = self.imagem_HSV[y,x]
                self.QT_HMin.setValue(max(0, H-self.fator_cor))
                self.QT_HMax.setValue(min(179, H+self.fator_cor))
                self.QT_SMin.setValue(max(0, S-self.fator_cor))
                self.QT_SMax.setValue(min(255, S+self.fator_cor))
                self.QT_VMin.setValue(max(0, V-self.fator_cor))
                self.QT_VMax.setValue(min(255, V+self.fator_cor))
                
                
            self.mudanca()
            
            
    def desenhar(self):
        img = self.referencia.copy()
        img2 = self.referencia.copy()
            
        img = cv2.drawContours(img2, self.contornos, -1, (255,0,0), 1)
        #img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Imagem.setPixmap(_qPixmap) 
        
        img = cv2.drawContours(np.zeros((img2.shape[0],img2.shape[1],3), np.uint8), self.contornos, -1, (255,0,0), -1)
        img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_PB.setPixmap(_qPixmap) 
        
        img = self.referencia.copy()
        img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
        for c in self.centroids:
            cv2.circle(img, (int(c[0]/2), int(c[1]/2)), 5, (255,0,0), -1)
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Contorno.setPixmap(_qPixmap) 
        
class GUI_centro(QMainWindow):
    def __init__(self):
        super(GUI_centro, self).__init__()
        loadUi('interface/centros.ui', self)
        self.show()    
        global VISAO
        self.dados = VISAO.read_Dados()
        
        self.getReferencia()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.mudanca)
        self.timer.start(1)
        
        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_btSalvar.clicked.connect(self.finalizar)
        
    def closeEvent(self, event):
    	self.timer.stop()
    	event.accept()
        
    def getReferencia(self):
        global VISAO
        self.referencia = VISAO.read_Imagem().imagem_crop
        self.centroids = VISAO.read_Imagem().centroids
        self.desenhar()
        
    def mudanca(self):
        self.dados.angCorr = self.QT_angCorr.value()/180.0*math.pi
        self.value_ang.setText("{0:.2f}º".format(self.dados.angCorr*180/math.pi))
        self.getReferencia()
        
    def finalizar(self):
        global VISAO
        VISAO.set_Dados(self.dados)
            
    def desenhar(self):
        centros = processamento.calculaCentros(self.centroids, self.dados.angCorr)
        
        img = self.referencia.copy()
        C = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p in zip(C, centros):
            cv2.circle(img, (int(p[0]), int(p[1])), 25, c, 1)
            cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(p[2])*50.0), int(p[1]+ math.sin(p[2])*50.0)), c, 3)
            cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(self.dados.angCorr)*50.0), int(p[1]+ math.sin(self.dados.angCorr)*50.0)), c, 1)
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_Imagem.setPixmap(_qPixmap)
    
class GUI_carregar(QMainWindow):
    def __init__(self):
        super(GUI_carregar, self).__init__()
        loadUi('interface/carregar.ui', self)
        self.show()    
        
        self.QT_listaSalvos.clear()
        for files in os.listdir("modelos"):
            if files.endswith(".red"):
                self.QT_listaSalvos.addItem(str(files))
        self.QT_carregar.clicked.connect(self.carregar)
     
    def carregar(self):
        global VISAO
        arquivo = open("modelos/" + self.QT_listaSalvos.currentText(), 'rb')
        VISAO.set_Dados(pickle.load(arquivo))
    
    
class GUI_salvar(QMainWindow):
    def __init__(self):
        super(GUI_salvar, self).__init__()
        loadUi('interface/salvar.ui', self)
        self.show()    
        self.QT_salvar.clicked.connect(self.salvar)
     
    def salvar(self):
        arquivo = open('modelos/' + self.QT_nomeSalvar.text() + '.red', 'wb')
        global VISAO
        pickle.dump(VISAO.read_Dados(), arquivo)
            
class GUI_camera(QMainWindow):
    def __init__(self):
        super(GUI_camera, self).__init__()
        loadUi('interface/camera.ui', self)
        self.show()    
        
        self.QT_listaVideos.clear()
        for files in os.listdir("videos"):
            if files.endswith(".avi"):
                self.QT_listaVideos.addItem(str(files))
        
        self.QT_camera.clicked.connect(self.setCamera)
        self.QT_video.clicked.connect(self.setVideo)
        self.QT_webcam.clicked.connect(self.setWebcam)
        
    def setCamera(self):
        global VISAO
        VISAO.alterarSrc(2)
        
    def setVideo(self):
        global VISAO
        VISAO.alterarSrc("videos/" + self.QT_listaVideos.currentText())
        
    def setWebcam(self):
        global VISAO
        VISAO.alterarSrc(0)


class GUI_controle(QMainWindow):
    def __init__(self):
            super(GUI_controle,self).__init__()
            loadUi('interface/controle.ui',self)
            self.show()

            self.inicializarValores()

            self.lineKd1.textChanged.connect(self.mudanca)
            self.lineKp1.textChanged.connect(self.mudanca)
            self.lineKi1.textChanged.connect(self.mudanca)
            self.lineKd2.textChanged.connect(self.mudanca)
            self.lineKp2.textChanged.connect(self.mudanca)
            self.lineKi2.textChanged.connect(self.mudanca)
            self.lineKd3.textChanged.connect(self.mudanca)
            self.lineKp3.textChanged.connect(self.mudanca)
            self.lineKi3.textChanged.connect(self.mudanca)
            self.porta_value.textChanged.connect(self.mudanca)
            self.esq_radio.toggled.connect(self.mudanca)
            self.dir_radio.toggled.connect(self.mudanca)
            self.bolaNossa.stateChanged.connect(self.mudanca)
            self.duasFaces.stateChanged.connect(self.mudanca)
            self.kalman.stateChanged.connect(self.mudanca)
            self.simular.stateChanged.connect(self.mudanca)
            self.alvoFixo.stateChanged.connect(self.mudanca)
            
            global VISAO
            VISAO.sincronizar_Controle()
            
    def mudanca(self):
            global VISAO
            DadosControle = VISAO.sincronizar_Controle()
            
            DadosControle.Kp1 = self.lineKp1.text()
            DadosControle.Kd1 = self.lineKd1.text()
            DadosControle.Ki1 = self.lineKi1.text()
            DadosControle.Kp2 = self.lineKp2.text()
            DadosControle.Kd2 = self.lineKd2.text()
            DadosControle.Ki2 = self.lineKi2.text()
            DadosControle.Kp3 = self.lineKp3.text()
            DadosControle.Kd3 = self.lineKd3.text()
            DadosControle.Ki3 = self.lineKi3.text()
            DadosControle.porta = self.porta_value.text()
            DadosControle.trocouCampo = True if self.dir_radio.isChecked() else False 
            DadosControle.bolaNossa1 = 1 if self.bolaNossa.isChecked() else 0 
            DadosControle.duasFaces = True if self.duasFaces.isChecked() else False 
            DadosControle.flagAtivaKalman = True if self.kalman.isChecked() else False 
            DadosControle.simular = True if self.simular.isChecked() else False 
            DadosControle.irParaAlvoFixo = True if self.alvoFixo.isChecked() else False 

            VISAO.set_DadosControle(DadosControle)

    def inicializarValores(self):
            global VISAO
            DadosControle = VISAO.sincronizar_Controle()  
                  
            self.lineKd1.setText(str(DadosControle.Kd1)) 
            self.lineKp1.setText(str(DadosControle.Kd1))
            self.lineKi1.setText(str(DadosControle.Ki1))
            self.lineKd2.setText(str(DadosControle.Kd2))
            self.lineKp2.setText(str(DadosControle.Kp2))
            self.lineKi2.setText(str(DadosControle.Ki2))
            self.lineKd3.setText(str(DadosControle.Kd3))
            self.lineKp3.setText(str(DadosControle.Kp3))
            self.lineKi3.setText(str(DadosControle.Ki3))
            self.porta_value.setText(DadosControle.porta)
            
            self.esq_radio.setChecked(DadosControle.trocouCampo) 
            self.bolaNossa.setChecked(DadosControle.bolaNossa1)
            self.duasFaces.setChecked(DadosControle.duasFaces) 
            self.kalman.setChecked(DadosControle.flagAtivaKalman)  
            self.simular.setChecked(DadosControle.simular) 
            self.alvoFixo.setChecked(DadosControle.irParaAlvoFixo)
    
class GUI_jogar(QMainWindow):
    def __init__(self):
        super(GUI_jogar,self).__init__()
        loadUi('interface/jogar.ui',self)
        self.show()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1)

        self.jogando = False
        self.rJogar.setChecked(True)
        self.btJogar.clicked.connect(self.AtivaSerial)
        self.rJogar.toggled.connect(self.mudanca)
        self.rParar.toggled.connect(self.mudanca)
        self.rPosInicial.toggled.connect(self.mudanca)
        
    def updateFrame(self):
        global VISAO
        Imagem = VISAO.read_Imagem()
        Dados = VISAO.read_Dados()
        DadosControle = VISAO.sincronizar_Controle_dinamico()

        img = Imagem.imagem_crop
        C = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p,a in zip(C, Imagem.centros,DadosControle.angulo_d):
            cv2.circle(img, (int(p[0]), int(p[1])), 20, c, 1)
            cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(p[2])*25), int(p[1]+ math.sin(p[2])*25)), c, 3) #Angulo Robo
            #cv2.line(img, (int(p[0]), int(p[1])), (int(p[0] + math.cos(Dados.angCorr)*50), int(p[1]+ math.sin(Dados.angCorr)*50)), c, 1)
            cv2.line(img,(int(p[0]),int(p[1])),(int(p[0]+math.cos(a)*25),int(p[1]+math.sin(a)*25)),(255,255,0),1) #Angulo controle

        C = [(55, 55, 55), (10, 10, 10), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for c, p in zip(C, Imagem.centroids):
            for _p in p[0]:
                cv2.circle(img, (int(_p[0]), int(_p[1])), 4, c, -1)
        _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        _qPixmap = QPixmap.fromImage(_qImage)
        self.QT_jogar.setPixmap(_qPixmap)



        if self.jogando:
            #Descomentar quando o controle estiver funcional
            #DadosControle = enviarInfo.InicializaControle(DadosControle)
            VISAO.set_DadosControle(DadosControle)
    
    def AtivaSerial(self):          
        global VISAO
        DadosControle = VISAO.read_DadosControle()
        if self.jogando:
                self.jogando = False
                self.btJogar.setText('Iniciar transmissao')
                self.btJogar.setStyleSheet("background-color:green")
                DadosControle.ser = 0
        else:
            try:
                #Descomentar quando em jogo
                #DadosControle.ser = serial.Serial(DadosControle.porta,DadosControle.velocidade)
                self.jogando = True
                self.btJogar.setText('Terminar transmissao')
                self.btJogar.setStyleSheet("background-color:red")
            except:
                logger().erro('Porta não encontrada')
                self.jogando = False
                self.btJogar.setText('Iniciar transmissao')
                self.btJogar.setStyleSheet("background-color:green")
                DadosControle.ser = 0

        VISAO.set_DadosControle(DadosControle)
        
    def closeEvent(self, event):
    	self.timer.stop()
    	event.accept()

    def mudanca(self):
        global VISAO
        DadosControle = VISAO.sincronizar_Controle_dinamico()
 
        DadosControle.Pjogar = True if self.rJogar.isChecked() else False
        DadosControle.Pparar = True if self.rParar.isChecked() else False
        DadosControle.Pinicial = True if self.rPosInicial.isChecked() else False
            
        VISAO.set_DadosControle(DadosControle)
           







if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI_main()
    window.show()
    sys.exit(app.exec_())
    

