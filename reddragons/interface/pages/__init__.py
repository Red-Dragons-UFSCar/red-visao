from .carregar import GUI_carregar
from .centros import GUI_centro
from .controle import GUI_controle
from .cores import GUI_cores
from .cruzetas import GUI_cruzetas
from .jogar import GUI_jogar
from .main import GUI_main
from .perspectiva import GUI_perspectiva
from .salvar import GUI_salvar
from .visualizacao import GUI_visualizacao
from .mainwindow import GUI_video
from .top import VisaoTop
from .kmeans import GUI_k_medians
from .juiz import GUI_juiz
routes = [
    ("carregar", GUI_carregar),
    ("centro", GUI_centro),
    ("controle", GUI_controle),
    ("kmeans", GUI_k_medians),
    ("cores", GUI_cores),
    ("cruzetas", GUI_cruzetas),
    ("jogar", GUI_jogar),
    ("main", GUI_main),
    ("perspectiva", GUI_perspectiva),
    ("salvar", GUI_salvar),
    ("visualizacao", GUI_visualizacao),
    ("video", GUI_video),
    ("juiz", GUI_juiz)
]

__all__ = [
    "GUI_carregar",
    "GUI_centro",
    "GUI_controle",
    "GUI_k_medians",
    "GUI_cores",
    "GUI_cruzetas",
    "GUI_jogar",
    "GUI_main",
    "GUI_perspectiva",
    "GUI_salvar",
    "GUI_visualizacao",
    "GUI_video",
    "GUI_juiz",
    "VisaoTop"
]
