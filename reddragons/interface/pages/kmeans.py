import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import reddragons.utils as vutils
from PyQt5.QtWidgets import QMainWindow
from ..utils import ui_files

class GUI_k_medians(QMainWindow):
    def __init__(self):
        super(GUI_k_medians, self).__init__()
        loadUi(f"{ui_files}/kmedians.ui", self)
        self.show()

        self.centroids = np.empty([0, 3])

        global VISAO
        self.k_ref = [[20, 103, 254], [101, 140, 255], [85, 125, 220], [176, 156, 255], [144, 26, 254], [28, 92, 255]]
        self.k_ref_pos=[[511, 210], [219, 200], [218, 189], [226, 267], [247, 269], [141, 175]]
        self.dados = VISAO.read_Dados()

        self.QT_AreaMax.setValue(self.dados.AreaMaxima)
        self.QT_AreaMin.setValue(self.dados.AreaMinimo)

        self.getReferencia()
        self.QT_btReferencia.clicked.connect(self.getReferencia)
        self.QT_bt_gerar_clusters.clicked.connect(self.gerar_clusters)
        self.QT_bt_isolar_clusters.clicked.connect(self.isolar_clusters)
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
        self.contornos, _ = vutils.get_contorno_cor(
            self.imagem_hsv, self.dados.cores[0], self.dados.filtros[0]
        )
        self.desenhar()

    def salvar(self):
        i = self.QT_selecao.currentIndex()
        self.dados.cores[i] = [[self.QT_HMin.value(), self.QT_SMin.value(), self.QT_VMin.value()],
                               [self.QT_HMax.value(), self.QT_SMax.value(), self.QT_VMax.value()]]
        self.dados.filtros[i] = [int(self.QT_qualKernel.currentIndex()), int(self.QT_tipoKernel.currentIndex()),
                                 self.QT_valorKernel.value()]

        self.dados.AreaMinimo = self.QT_AreaMin.value()
        self.dados.AreaMaxima = self.QT_AreaMax.value()
        global VISAO
        VISAO.set_Dados(self.dados)

    def novaCor(self):
        i = self.QT_selecao.currentIndex()
        self.contornos, _ = processamento.getContornoCor(self.imagem_HSV, self.dados.cores[i], self.dados.filtros[i])

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

        self.dados.cores[i] = [[self.QT_HMin.value(), self.QT_SMin.value(), self.QT_VMin.value()],
                               [self.QT_HMax.value(), self.QT_SMax.value(), self.QT_VMax.value()]]
        self.dados.filtros[i] = [int(self.QT_qualKernel.currentIndex()), int(self.QT_tipoKernel.currentIndex()),
                                 self.QT_valorKernel.value()]

        self.contornos, _ = processamento.getContornoCor(cv2.cvtColor(np.uint8(self.referencia), cv2.COLOR_RGB2HSV),
                                                         self.dados.cores[i], self.dados.filtros[i])

        self.centroids = np.empty([0, 3])
        for c in self.contornos:
            M = cv2.moments(c)
            if ((M["m00"] >= self.QT_AreaMin.value()) and (M["m00"] <= self.QT_AreaMax.value())):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                self.centroids = np.append(self.centroids, [[cX, cY, M["m00"]]], axis=0)

        self.desenhar()

    def gerar_clusters(self):
        get_cluster_means(self)

    def isolar_clusters(self):
        isolarClusters()

    def mouseReleaseEvent(self, QMouseEvent):
        _x = QMouseEvent.x()
        _y = QMouseEvent.y()
        x = _x - self.QT_Imagem.pos().x()
        y = _y - self.QT_Imagem.pos().y()

        if (x < self.QT_Imagem.geometry().width()) and (y < self.QT_Imagem.geometry().height() and x >= 0 and y >= 0):
            # logger().variavel("Cor no ponto ({0}, {1})".format(x,y), "RGB {0} HSV {1}".format(self.referencia[y, x], self.imagem_HSV[y, x]))
            if y > self.fator_clique and x > self.fator_clique and x < 640 - self.fator_clique and y < 480 - self.fator_clique:

                ref =self.imagem_HSV[y, x]
                i = self.QT_selecao.currentIndex()
                self.k_ref[i]=[ref[0],ref[1],ref[2]]
                self.k_ref_pos[i] = [x,y]
                print("i "+str(i)+" ref"+str(self.k_ref))
                drawReferences(self)
                # h, s,v = cv2.split(self.imagem_HSV)
                h=self.imagem_HSV[:, :, 0]
                h=h.ravel()
                s = self.imagem_HSV[:, :, 1]
                s = h.ravel()
                raio = 40
                minimo,maximo =[100,100,100],[155,155,155] #get_cluster_means(self,ref,self.imagem_HSV,raio=raio)
                print("min "+str(minimo)+" max "+str(maximo))
                HMin=max(0, minimo[0] )
                HMax = min(179, maximo[0] )
                self.QT_HMin.setValue(HMin)
                self.QT_HMax.setValue(HMax)
                SMin = max(0, minimo[1])
                SMax = min(255, maximo[1])
                self.QT_SMin.setValue(SMin)
                self.QT_SMax.setValue(SMax)
                print("----------------------------")
                print("v")
                VMin = max(0, minimo[2])
                VMax = min(255, maximo[2])
                self.QT_VMin.setValue(VMin)
                self.QT_VMax.setValue(VMax)
            else:
                H, S, V = self.imagem_HSV[y, x]
                self.QT_HMin.setValue(max(0, H - self.fator_cor))
                self.QT_HMax.setValue(min(179, H + self.fator_cor))
                self.QT_SMin.setValue(max(0, S - self.fator_cor))
                self.QT_SMax.setValue(min(255, S + self.fator_cor))
                self.QT_VMin.setValue(max(0, V - self.fator_cor))
                self.QT_VMax.setValue(min(255, V + self.fator_cor))

            self.mudanca()


    def desenhar(self):
            img = self.referencia.copy()
            img2 = self.referencia.copy()

            img = cv2.drawContours(img2, self.contornos, -1, (255, 0, 0), 1)
            # img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_Imagem.setPixmap(_qPixmap)

            img = cv2.drawContours(np.zeros((img2.shape[0], img2.shape[1], 3), np.uint8), self.contornos, -1, (255, 0, 0),
                                   -1)
            img = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_PB.setPixmap(_qPixmap)

            img = self.referencia.copy()
            img = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))
            for c in self.centroids:
                cv2.circle(img, (int(c[0] / 2), int(c[1] / 2)), 5, (255, 0, 0), -1)
            _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            self.QT_Contorno.setPixmap(_qPixmap)

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.uic import loadUi
import statistics
from enum import Enum
import datetime
from functools import partial
import cv2
import numpy as np
import copy
# import enviarInfo
# from from reddragons.estruturas import *
# from reddragons.logger import *
# import captura
# import reddragons.processamento
import serial

import sys
import pickle
import math

import glob, os
global kmeans_centers
global kmeans_centers_actives
global kmeans_window
global kmeans_label
global kmeans_image
global kmeans_image_result
global kmeans_colors_references
global kmeans_colours_buttons

def get_cluster_means(self):
    img = self.imagem_HSV
    mask = cv2.inRange(img,(0,0,0), (180,30,133))
    mask= cv2.bitwise_not(mask)
    img=cv2.bitwise_and(img, img, mask=mask)
    Z = img.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 60
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    global kmeans_colors_references
    kmeans_colors_references=self.k_ref
    # Now convert back into uint8, and make original image
    default_centers = []
    width= self.imagem_HSV.shape[1]
    for aux_pos in self.k_ref_pos:
        pos=width*aux_pos[1]+aux_pos[0]
        default_centers.append(int(label[pos]))
    index = 0
    center_colors=[]
    center_no_cut = copy.deepcopy(center)
    for i in center:
        if index not in default_centers:
            center[index-1]=[0,0,0]
        else:
            center_colors.append([i[0],i[1],i[2]])
        index+=1
    drawCentersKmeans(self,center_no_cut)

    res = center[label.flatten()]
    res_no_cut = center_no_cut[label.flatten()]
    res2 = res.reshape((img.shape))
    res_no_cut2_hsv = res_no_cut.reshape((img.shape))
    res_no_cut2= cv2.cvtColor(res_no_cut2_hsv, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    global kmeans_centers
    kmeans_centers= copy.deepcopy(center_no_cut)
    global kmeans_centers_actives
    kmeans_centers_actives = copy.deepcopy(center_no_cut)
    global  kmeans_window
    kmeans_window=self
    global  kmeans_label
    kmeans_label=label
    global  kmeans_image
    global kmeans_image_result
    kmeans_image=img
    kmeans_image_result = res_no_cut2
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def kmeans_color_clicked(button_qt,id):
    global kmeans_centers
    global kmeans_centers_actives
    if(button_qt.activated):
        button_qt.setStyleSheet("background-color: red")
        button_qt.activated=False
        kmeans_centers_actives[id]=[0,0,0]
    else:
        button_qt.setStyleSheet("background-color: green")
        button_qt.activated = True
        kmeans_centers_actives[id] =kmeans_centers[id]
    global  kmeans_window
    drawOnlyCentersKmeans( kmeans_window,kmeans_centers_actives)


def kmeans_color_set(button_qt,id,activate):
    global kmeans_centers
    global kmeans_centers_actives
    if(not activate):
        button_qt.setStyleSheet("background-color: red")
        button_qt.activated=False
        kmeans_centers_actives[id]=[0,0,0]
    else:
        button_qt.setStyleSheet("background-color: green")
        button_qt.activated = True
        kmeans_centers_actives[id] =kmeans_centers[id]




def isolarClusters():
    global kmeans_colors_references
    dist_aux=255
    id= -1
    new_centers = [None]*len(kmeans_colors_references)
    count = 0
    global kmeans_colours_buttons

    for center in kmeans_centers:
        kmeans_color_set(kmeans_colours_buttons[count], count,False)
        count +=1
    count = 0

    for color_reference in kmeans_colors_references:
        count_aux = 0
        dist_aux = 255
        for center in kmeans_centers:
            tempDist= np.linalg.norm(color_reference-center)
            if (tempDist<dist_aux):
                dist_aux=tempDist
                new_centers[count]=center
                id=count_aux
            count_aux+=1
        kmeans_color_set(kmeans_colours_buttons[id], id, True)
        count+=1
    global  kmeans_window
    global kmeans_centers_actives
    drawOnlyCentersKmeans( kmeans_window,kmeans_centers_actives)



def drawOnlyCentersKmeans(self,centers):
    global kmeans_label, kmeans_image,kmeans_image_result
    res = centers[kmeans_label.flatten()]
    res_no_cut = centers[kmeans_label.flatten()]
    res_no_cut2_hsv = res_no_cut.reshape((kmeans_image.shape))
    res_no_cut2 = cv2.cvtColor(res_no_cut2_hsv, cv2.COLOR_HSV2RGB)
    img = res_no_cut2
    _qImage = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
    _qPixmap = QPixmap.fromImage(_qImage)
    self.QT_Imagem.setPixmap(_qPixmap)

    kmeans_image_result=res_no_cut2

def drawCentersKmeans(self,centers):
    height = 40
    width = 70
    bytesPerLine = 3 * width
    blank_image = np.zeros((height, width, 3), np.uint8)

    count = 1
    global kmeans_colours_buttons
    kmeans_colours_buttons=[]
    for center in centers:
        q_cent = self.findChild(QPushButton, "QT_cent_"+str(count))
        if(q_cent):
            blank_image[:, :] = (center[0], center[1],center[2])
            blank_image = cv2.cvtColor(blank_image, cv2.COLOR_HSV2RGB)
            _qImage = QImage(blank_image, blank_image.shape[1], blank_image.shape[0], bytesPerLine, QImage.Format_RGB888)
            _qPixmap = QPixmap.fromImage(_qImage)
            q_cent.setIcon(QtGui.QIcon(_qPixmap))
            q_cent.setIconSize(QtCore.QSize(35, 25))
            q_cent.setStyleSheet("background-color: green")
            q_cent.clicked.connect(partial(kmeans_color_clicked,q_cent,count-1))
            q_cent.activated=True
            kmeans_colours_buttons.append(q_cent)
        count+=1




def drawReferences(self):
    height = 40
    width = 70
    bytesPerLine = 3 * width
    blank_image = np.zeros((height, width, 3), np.uint8)

    blank_image[:, :] = (self.k_ref[0][0], self.k_ref[0][1], self.k_ref[0][2])
    blank_image = cv2.cvtColor(blank_image, cv2.COLOR_HSV2RGB)
    _qImage = QImage(blank_image, blank_image.shape[1], blank_image.shape[0], bytesPerLine, QImage.Format_RGB888)
    _qPixmap = QPixmap.fromImage(_qImage)
    self.QT_ref_bola.setPixmap(_qPixmap)

    blank_image[:, :] = (self.k_ref[1][0], self.k_ref[1][1], self.k_ref[1][2])
    blank_image = cv2.cvtColor(blank_image, cv2.COLOR_HSV2RGB)
    _qImage = QImage(blank_image, blank_image.shape[1], blank_image.shape[0], bytesPerLine, QImage.Format_RGB888)
    _qPixmap = QPixmap.fromImage(_qImage)
    self.QT_ref_principal.setPixmap(_qPixmap)

    blank_image[:, :] = (self.k_ref[2][0], self.k_ref[2][1], self.k_ref[2][2])
    blank_image = cv2.cvtColor(blank_image, cv2.COLOR_HSV2RGB)
    _qImage = QImage(blank_image, blank_image.shape[1], blank_image.shape[0], bytesPerLine, QImage.Format_RGB888)
    _qPixmap = QPixmap.fromImage(_qImage)
    self.QT_ref_goleiro.setPixmap(_qPixmap)

    blank_image[:, :] = (self.k_ref[3][0], self.k_ref[3][1], self.k_ref[3][2])
    blank_image = cv2.cvtColor(blank_image, cv2.COLOR_HSV2RGB)
    _qImage = QImage(blank_image, blank_image.shape[1], blank_image.shape[0], bytesPerLine, QImage.Format_RGB888)
    _qPixmap = QPixmap.fromImage(_qImage)
    self.QT_ref_zagueiro.setPixmap(_qPixmap)

    blank_image[:, :] = (self.k_ref[4][0], self.k_ref[4][1], self.k_ref[4][2])
    blank_image = cv2.cvtColor(blank_image, cv2.COLOR_HSV2RGB)
    _qImage = QImage(blank_image, blank_image.shape[1], blank_image.shape[0], bytesPerLine, QImage.Format_RGB888)
    _qPixmap = QPixmap.fromImage(_qImage)
    self.QT_ref_atacante.setPixmap(_qPixmap)

    blank_image[:, :] = (self.k_ref[5][0], self.k_ref[5][1], self.k_ref[5][2])
    blank_image = cv2.cvtColor(blank_image, cv2.COLOR_HSV2RGB)
    _qImage = QImage(blank_image, blank_image.shape[1], blank_image.shape[0], bytesPerLine, QImage.Format_RGB888)
    _qPixmap = QPixmap.fromImage(_qImage)
    self.QT_ref_adversario.setPixmap(_qPixmap)