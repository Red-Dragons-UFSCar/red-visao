import json
import numpy as np

def parse_square (points):
    """recebe 4 coordenadas e ordena em sentido horario a partir do vertice superior esquerdo

    Parameters
    ----------
    points : list of tuple of int
        pontos a serem ordenados

    Returns
    -------
    list of tuple of int
        pontos ordenados    
    """
    get_y = lambda x: x[1] 
    get_x = lambda x: x[0] 
    y_sorted = sorted(points, key=get_y)
    top = y_sorted[:2]
    bottom = y_sorted[2:]
    return sorted(top, key=get_x) + sorted(bottom, key=get_x)

def intersec (pts1, pts2):
    """identifica interseccao entre duas retas

    Parameters
    ----------
    pts1 : list of list of int
        dois pontos contidos na primeira reta ex: ((x1,y1), (x2,y2)) 
    pts2 : list of list of int
        dois pontos contidos na segunda reta ex: ((x1,y1), (x2,y2)) 

    Returns
    -------
    list of int
        ponto de interseccao (x,y)
    """
    a = np.array([[(pts1[1][0]-pts1[0][0]), (pts2[0][0]-pts2[1][0])],
         [(pts1[1][1]-pts1[0][1]), (pts2[0][1]-pts2[1][1])]])
    b = np.array([(pts2[0][0]-pts1[0][0]),
         (pts2[0][1]-pts1[0][1])])
    x = np.linalg.solve(a,b)
    is_x = pts1[0][0]+x[0]*(pts1[1][0]-pts1[0][0])
    is_y = pts1[0][1]+x[0]*(pts1[1][1]-pts1[0][1])
    return tuple([int(is_x), int(is_y)])

class PointsParser:

    def __init__ (self, pontos):
        self._pontos = pontos

    def _divide (self):
        y_sorted = sorted(self._pontos, key=lambda x: x[1])
        self.campo = y_sorted[:2] + y_sorted[-2:] 
        self.campo = parse_square (self.campo)
        self.gol = y_sorted[2:-2]
        self.gol = parse_square (self.gol)
    
    def _get_pontos_externos (self):
        gol_esq = [self.gol[0], self.gol[2]]
        gol_dir = [self.gol[1], self.gol[3]]
        self.pontos_externos = []
        self.pontos_externos.append(intersec(self.campo[:2], gol_esq))
        self.pontos_externos.append(intersec(self.campo[:2], gol_dir))
        self.pontos_externos.append(intersec(self.campo[2:], gol_esq))
        self.pontos_externos.append(intersec(self.campo[2:], gol_dir))

    def _get_pontos_internos (self):
        campo_esq = [self.campo[0], self.campo[2]]
        campo_dir = [self.campo[1], self.campo[3]]
        self.pontos_internos = []
        self.pontos_internos.append(intersec(self.gol[:2], campo_esq))
        self.pontos_internos.append(intersec(self.gol[:2], campo_dir))
        self.pontos_internos.append(intersec(self.gol[2:], campo_esq))
        self.pontos_internos.append(intersec(self.gol[2:], campo_dir))

    def run(self):
        self._divide()
        self._get_pontos_externos()
        self._get_pontos_internos()
        
        self.final = {
            "campo": self.campo,
            "gol" : self.gol,
            "internos": self.pontos_internos,
            "externos": self.pontos_externos,
        }
        return self.final
    
    def save (self, filename):
        with open (filename, 'w') as f:
            json.dump (self.final, f)

