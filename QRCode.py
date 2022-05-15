from os import remove
import tkinter as tk
from unittest import case
import PIL as pil
from PIL import Image
from PIL import ImageTk 
from tkinter import filedialog
from tkinter import simpledialog
import numpy as np
from copy import deepcopy


def nbrCol(matrice):
    return(len(matrice[0]))

def nbrLig(matrice):
    return len(matrice)
    
def saving(matPix, filename):#sauvegarde l'image contenue dans matpix dans le fichier filename
							 #utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)

def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
					  #l'image en noir et blanc
    toLoad=pil.Image.open(filename)
    m=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            m[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return m


QRMatrix = [[1 for j in range(25)] for i in range(25)]


def QRSkeleton(m):
    squareInQrcode(m)
    for i in range(6, len(m)-7, 2):
        m[i][6] = 0
        m[6][i] = 0



def squareInQrcode(m):
    """créattion squelette de la matrice"""
    for i in range(len(m)):
        if i == 0 or i == 6:
            for j in range(len(m)):
                if (j >= 0 and j <= 6) or (j >= len(m)-7 and j <= len(m)-1): 
                    m[i][j] = 0
        elif i == len(m)-7 or i == len(m)-1:
            for j in range(7):
                m[i][j] = 0
        elif (i >= 2 and i <= 4):
            for j in range(7):
                if j == 1 or j == 5:
                    continue
                else:
                    m[i][j] = 0
                    m[i][len(m)-1-j] = 0
        elif (i >= len(m)-5 and i <= len(m)-3):
            for j in range(7):
                if j == 1 or j == 5:
                    continue
                else:
                    m[i][j] = 0
        elif i == 1 or i == 5:
            m[i][0] = 0
            m[i][6] = 0
            m[i][len(m)-7] = 0
            m[i][len(m)-1] = 0
        elif i == len(m)-6 or i == len(m)-2:
            m[i][0] = 0
            m[i][6] = 0


def _rotate(m):
    """vérification du sens de la matrice"""
    global QRMatrix
    res = True
    n = len(m)-1
    for i in range(len(m)-7, len(m)):
        for j in range(len(m)-7, len(m)):
            if i == n-6 or i == n:
                if m[i][j] != 0:
                    res = False
                    break
            elif i == n-5 or i == n-1:
                if j == n-6 or j == n:
                    if m[i][j] != 0:
                        res = False
                        break
                elif j >=n-5 and j <= n-1:
                    if m[i][j] != 1:
                        res = False
                        break
            elif i >= n-4 and i <= n-2:
                if j == n-6 or j == n or (j >=n-4 and j <= n-2):
                    if m[i][j] != 0:
                        res = False
                        break
                else:
                    if m[i][j] != 1:
                        res = False
                        break

        if not res:
            break
    print(res)
    return res

def rotate():
    global QRMatrix
    """rotation à droite de la matrice tant qu'elle n'est pas dans le bon sens"""
    aux = [[1] *(len(QRMatrix)) for j in range(len(QRMatrix))]
    test =_rotate(QRMatrix)
    while test:
        print("coucou")
        print("----------------------------------------------------------------------------------------------------------------------------------------")
        for i in range(len(QRMatrix)):
            for j in range(len(QRMatrix)):
                aux[i][j] = QRMatrix[len(QRMatrix)-j-1][i]
        QRMatrix = deepcopy(aux) 
        printBeautifulMatrice(QRMatrix)
        test =_rotate(QRMatrix)
        

 

    

def rotate2():
    global QRMatrix
    """rotation à droite de la matrice tant qu'elle n'est pas dans le bon sens"""
    aux = [[1] *(len(QRMatrix)) for j in range(len(QRMatrix))]

    for i in range(len(QRMatrix)):
        for j in range(len(QRMatrix)):
            aux[i][j] = QRMatrix[len(QRMatrix)-j-1][i]

    QRMatrix = aux.copy()
  

    
def decimalToBinary3bits(n):
    """convertie une valeur décimale en binaire sur 3 bits"""
    res = []
    n = bin(n).replace("0b", "")
    while len(n) < 3:
        n = '0' + n
    for e in n:
        res.append(e)
    return res

def code_de_Hamming(liste=[]):
    """
    Fonction qui va prendre en paramètre une liste de 7 bits
    et va vérifier s'il y a ou non une erreur 
    si oui il va la corriger
    Va retourner les 4 bits d'informations et également la liste avec mofication erreur si il y en a une.
    Réutilisation de la fonction que l'on a travailler en TD.
    """
    liste_message = []
    # Calcul des bits de parités. 
    # Regarde si ils ont la bonne valeur
    c_1=(liste[4] == (liste[0] + liste[1] + liste[3])%2)
    c_2=(liste[5] == (liste[0] + liste[2] + liste[3])%2)
    c_3=(liste[6] == (liste[1] + liste[2] + liste[3])%2)
    
    # Si un des ou plusieurs bits de parité à une valeur différente ont va modifier le bit erroné
    if(not c_1 and not c_2 and not c_3):
        liste[3]=(liste[3]+1)%2
    elif(not c_1 and not c_2):
        liste[0]=(liste[0]+1)%2
    elif(not c_1 and not c_3):
        liste[1]=(liste[1]+1)%2
    elif(not c_2 and not c_3):
        liste[2]=(liste[2]+1)%2
    elif(not c_1):
        liste[4]=(liste[4]+1)%2
    elif(not c_2):
        liste[5]=(liste[5]+1)%2
    elif(not c_3):
        liste[6]=(liste[6]+1)%2

    for i in range(4): 
        liste_message.append(liste[i])
    return liste_message

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


def readBlock(m):
    res = []
    i, j = len(m)
    while len(res) < 14:
        res.append(m[i][j])
        if i > j:
            i +=1
            j -= 1
        else:
            i -=1
    return res


def conversion_binaire_entier(liste_donnees):
    """
    Fonction qui va convertir une listes de bits en un entier
    Réutilisation d'une fonction que l'on a vu en TP. 
    """
    nombre_entier = 0
    for a in range(len(liste_donnees)):
        nombre_entier += (liste_donnees[a]*(2**(len(liste_donnees)-a-1)))
    return nombre_entier



def decoupage46bits(listebits, nbr_elements):
    """ 
    Va découper la liste en différentes partie avec juste
    4 éléments par partie.
    Retourne la liste des différentes parties. 
    """
    res = []
    for i in range(0, len(listebits), nbr_elements):
        res.append(listebits[i:(i+nbr_elements)])
  
    return res    

def filtre(QRCode_matrice):
    if QRCode_matrice[23][8] == 0 and QRCode_matrice[22][8] == 0:
        # filtre noire
        return QRCode_matrice
    if QRCode_matrice[23][8] == 0 and QRCode_matrice[22][8] == 1:
        # filte damier
        QRMatrix_avec_filte = filtre_damier(QRCode_matrice) 
    if QRCode_matrice[23][8] == 1 and QRCode_matrice[22][8] == 0:
        # filtre horizontales
        QRMatrix_avec_filte = filtre_horizontales(QRCode_matrice) 
    if QRCode_matrice[23][8] == 1 and QRCode_matrice[22][8] == 1:
        # filtre verticales
        QRMatrix_avec_filte = filtre_verticales(QRCode_matrice) 

    return QRCode_matrice


def filtre_damier(QRCode_matrice):
    b = 0
    for i in range(nbrLig(QRCode_matrice)):
        for j in range(nbrCol(QRCode_matrice)):
            if j >= 7 and i <= 7 :
                print(QRCode_matrice[i][j])
                QRCode_matrice[i][j] = QRCode_matrice[i][j] ^ b % 2
                print(QRCode_matrice[i][j])
                b += 1

    
    
    return QRCode_matrice

def filtre_horizontales(QRCode_matrice):
    b = 0
    for i in range(nbrLig(QRCode_matrice)):
        for j in range(nbrCol(QRCode_matrice)):
            if 24 > j > 7 and 0 <= i <= 7:
                QRCode_matrice[i][j] ^= b % 2
                b += 1
            elif 24 > i > 7 and 0 <= j <= 7:
                QRCode_matrice[i][j] ^= b % 2
                b += 1
    return QRCode_matrice


def filtre_verticales(QRCode_matrice):
    for i in range(nbrLig(QRCode_matrice)):
        for j in range(nbrCol(QRCode_matrice)):
            if 24 > j > 7 and 0 <= i <= 7:
                QRCode_matrice[i][j] ^= j % 2
            elif 24 > i > 7 and 0 <= j <= 7:
                QRCode_matrice[i][j] ^= j % 2
    
    
    return QRCode_matrice
    
def printBeautifulMatrice(a):
    for line in a:
        print('   '.join(map(str, line)))


QRSkeleton(QRMatrix)
#printBeautifulMatrice(rotate(QRSkeleton(QRMatrix)))
rotate2()



printBeautifulMatrice(QRMatrix)
rotate()
print("--------------------------------------------------------------------------------")
