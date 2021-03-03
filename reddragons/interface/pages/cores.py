from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files
from PyQt5.uic import loadUi

import cv2
import numpy as np

from reddragons.visao.logger import *
from reddragons.visao import processamento

class GUI_cores(QMainWindow):
    def __init__(self, visao):
        super(GUI_cores, self).__init__()
        loadUi(f'{ui_files}/cores.ui', self)
        self.show()
        self.visao = visao
        self.centroids = np.empty([0,3])
        
        
        self.dados = self.visao.read_Dados()
        
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
        
        self.referencia = self.visao.read_Imagem().imagem_crop
        self.imagem_HSV = self.visao.read_Imagem().imagem_HSV
        self.dados = self.visao.read_Dados()
        self.contornos, _ = processamento.getContornoCor(self.imagem_HSV, self.dados.cores[0], self.dados.filtros[0])
        self.desenhar()
        
    def salvar(self):
        i = self.QT_selecao.currentIndex()
        self.dados.cores[i] = [ [self.QT_HMin.value(), self.QT_SMin.value(), self.QT_VMin.value()], [self.QT_HMax.value(), self.QT_SMax.value(), self.QT_VMax.value()]]
        self.dados.filtros[i] = [ int(self.QT_qualKernel.currentIndex()), int(self.QT_tipoKernel.currentIndex()), self.QT_valorKernel.value()]
        
        self.dados.AreaMinimo = self.QT_AreaMin.value()
        self.dados.AreaMaxima = self.QT_AreaMax.value()
        
        self.visao.set_Dados(self.dados)
        
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
