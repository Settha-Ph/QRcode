from os import remove
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

    
def decimalToBinary3bits(n):
    """convertie une valeur décimale en binaire sur 3 bits"""
    res = []
    n = bin(n).replace("0b", "")
    while len(n) < 3:
        n = '0' + n
    for e in n:
        res.append(e)
    return res



def correction(l):
    t = len(l)
    l_pos = []
    l_bin = []
    aux = 0
    for i in range(len(l)):
        if l[i] == 1:
            print(t - i)
            l_pos.append(t-i)
    for e in l_pos:
        l_bin.append(decimalToBinary3bits(e))
    for i in range(len(l_bin)):
        pair = 0
        for j in range(len(l_bin)):
            pair += l_bin[j][i]
        if pair % 2 != 0:
            if i == 0:
                aux += 4
            if i == 1:
                aux += 2
            else:
                aux += 1
    if aux != 0:
        l[t - aux - 1 ] = 1 if l[t - aux - 1] == 0 else 0 
    return [l[0], [1], l[2], l[4]]


def readImage(m):
    res = []
    i, j = len(m)
    while len(res) < 14:
        res.append(m[i][j])
        
    

    pass
        
    

    
    
#correction([1, 1, 0, 0, 0, 1, 0])
print(decimalToBinary3bits(3))
 


        
            
            


def printBeautifulMatrice(a):
    for line in a:
        print('  '.join(map(str, line)))



#QRSkeleton(QRMatrix)
#printBeautifulMatrice(QRMatrix)
