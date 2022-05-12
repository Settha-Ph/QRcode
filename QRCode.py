import tkinter as tk
from unittest import case
import PIL as pil
from PIL import Image
from PIL import ImageTk 
from tkinter import filedialog
from tkinter import simpledialog
import numpy as np


QRMatrix = [[0 for j in range(25)] for i in range(25)]


def QRSkeleton(m):
    squareInQrcode(m)
    for i in range(6, len(m)-7, 2):
        m[i][6] = 1
        m[6][i] = 1



def squareInQrcode(m):
    """créattion squelette de la matrice"""
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
        

def _rotate(m):
    """vérification du sens de la matrice"""
    res = True
    n = len(m)-1
    for i in range(7):
        for j in range(7):
            if i == n-6 or i == n:
                if m[i][j] != 1:
                    res = False
                    break
            elif i == n-5 or i == n-1:
                if j == n-6 or j == n:
                    if m[i][j] != 1:
                        res = False
                        break
                elif j >=n-5 and j <= n-1:
                    if m[i][j] != 0:
                        res = False
                        break
            elif i >= n-4 and i <= n-2:
                if j == n-6 or j == n or (j >=n-4 and j <= n-2):
                    if m[i][j] != 1:
                        res = False
                        break
                else:
                    if m[i][j] != 0:
                        res = False
                        break

        if not res:
            break
    return res


def rotate(m):
    """rotation à droite de la matrice tant qu'elle n'est pas dans le bon sens"""
    while not _rotate(m):
        for i in range(len(m)):
            for j in range(len(m)):
                m[i][j] = m[len(m)-j-1][i]

def decimalToBinary():
    


def correction(l):
    l_aux = []
    for i in range(len(l)):
        if l[i] == 1:
            print(len(l) - i)
            l_aux.append(len(l)-i)
    
    
correction([1, 1, 0, 0, 0, 1, 0])
    


        
            
            


def printBeautifulMatrice(a):
    for line in a:
        print('  '.join(map(str, line)))



#QRSkeleton(QRMatrix)
#printBeautifulMatrice(QRMatrix)
