from __future__ import annotations
from typing import Optional

import os
from inspect import getframeinfo, stack

from colorama import Fore, Back, Style


class SingletonMeta(type):
    _instance: Optional[Singleton] = None

    def __call__(self) -> Singleton:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class logger(metaclass=SingletonMeta):
    def limpar(self):
        os.system("clear")

    def erro(self, err):
        self.escrever(Fore.RED, err, "ERRO")

    def dado(self, dado):
        self.escrever(Fore.CYAN, dado, "DADO")

    def flag(self, dado):
        self.escrever(Fore.BLUE, dado, "FLAG")

    def variavel(self, var, valor):
        self.escrever(Fore.GREEN, str(valor), var)

    def escrever(self, cor, info, texto_aux):
        caller = getframeinfo(stack()[2][0])

        print(
            Style.BRIGHT
            + os.path.basename(caller.filename)
            + Style.NORMAL
            + ":{0}:{1}\t".format(caller.function, caller.lineno)
            + cor
            + Style.BRIGHT
            + texto_aux
            + Style.NORMAL
            + ": "
            + info
            + Style.RESET_ALL
        )

    def tempo(
        self,
        i_frame,
        tempoInicial,
        tempoCamera,
        tempoCopia,
        tempoWarp,
        tempoCorte,
        tempoHSV,
        tempoCentroids,
        tempoCentros,
        tempoFinal,
    ):
        total = 100.0 / (tempoFinal - tempoInicial)
        print(
            Style.BRIGHT
            + "FRAME "
            + str(i_frame)
            + Style.NORMAL
            + "\nCâmera:  {0:.4f}s [{1:5.2f}%]\tCopia: {2:.4f}s [{3:5.2f}%]\t\tWarp: {4:.4f}s [{5:5.2f}%]\t\tCorte: {6:.4f}s [{7:5.2f}%]\nHSV:\t {8:.4f}s [{9:5.2f}%]\tCentroids: {10:.4f}s [{11:5.2f}%]\tCentros: {12:.4f}s [{13:5.2f}%]\n".format(
                tempoCamera - tempoInicial,
                (tempoCamera - tempoInicial) * total,
                tempoCopia - tempoCamera,
                (tempoCopia - tempoCamera) * total,
                tempoWarp - tempoCopia,
                (tempoWarp - tempoCopia) * total,
                tempoCorte - tempoWarp,
                (tempoCorte - tempoWarp) * total,
                tempoHSV - tempoCorte,
                (tempoHSV - tempoCorte) * total,
                tempoCentroids - tempoHSV,
                (tempoCentroids - tempoHSV) * total,
                tempoCentros - tempoCentroids,
                (tempoCentros - tempoCentroids) * total,
            )
            + Style.BRIGHT
            + "Total: {0:.4f}s  {1:.0f}ms\t\tFPS: {2:.4f}\n".format(
                tempoFinal - tempoInicial,
                1000.0 * (tempoFinal - tempoInicial),
                1.0 / (tempoFinal - tempoInicial),
            )
            + Style.NORMAL
        )
