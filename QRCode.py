import tkinter as tk
from unittest import case
import PIL as pil
from PIL import Image
from PIL import ImageTk 
from tkinter import filedialog
from tkinter import simpledialog
import numpy as np


QRMatrix = [[0 for j in range(25)] for i in range(25)]


def QRSkeleton():
    pass


def squareInQrcode(m):
    for i in range(len(m)):
        if i == 0 or i == 6:
            for j in range(len(m)):
                if (j >= 0 and j <= 6) or (j >= len(m)-7 and j <= len(m)-1): 
                    m[i][j] = 1
        elif i == len(m)-7 or i == len(m)-1:
            for j in range(7):
                m[i][j] = 1
        elif (i >= 2 and i <= 4):
            for j in range(7):
                if j == 1 or j == 5:
                    continue
                else:
                    m[i][j] = 1
                    m[i][len(m)-1-j] = 1
        elif (i >= len(m)-5 and i <= len(m)-2):
            for j in range(7):
                if j == 1 or j == 5:
                    continue
                else:
                    m[i][j] = 1
        elif i == 1 or i == 5:
            m[i][0] = 1
            m[i][6] = 1
            m[i][len(m)-7] = 1
            m[i][len(m)-1] = 1
        elif i == len(m)-6 or i == len(m)-2:
            m[i][0] = 1
            m[i][6] = 1
        
            


def printBeautifulMatrice(a):
    for line in a:
        print('  '.join(map(str, line)))



squareInQrcode(QRMatrix)
printBeautifulMatrice(QRMatrix)
