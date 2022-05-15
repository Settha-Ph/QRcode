from itertools import count
from os import remove
import tkinter as tk
from unittest import case
import PIL as pil
from PIL import Image
from PIL import ImageTk 
from tkinter import N, filedialog
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
    return res

def rotate():
    global QRMatrix
    """rotation à droite de la matrice tant qu'elle n'est pas dans le bon sens"""
    aux = [[1] *(len(QRMatrix)) for j in range(len(QRMatrix))]
    test =_rotate(QRMatrix)
    while test:
        for i in range(len(QRMatrix)):
            for j in range(len(QRMatrix)):
                aux[i][j] = QRMatrix[len(QRMatrix)-j-1][i]
        QRMatrix = deepcopy(aux) 
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

"""
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
"""

def readInBlock(m, i, j):
    """lecture dans un bloc de droite à gauche"""
    res = []
    aux = []
    phase = 0
    while len(res) < 14:
        res.append(m[i][j])
        if phase == 1:
            i +=1
            j -= 1
            phase -= 1
        else:
            i -=1
            phase += 1
    aux1 = code_de_Hamming(res[:7])
    aux2 = code_de_Hamming(res[7:])
    aux = aux1 + aux2
    
    return aux

def readInBlock2(m, i, j):
    """lecture dans un bloc de gauche à droite"""
    res = []
    phase = 0
    while len(res) < 14:
        res.append(m[i][j])
        if phase == 1:
            i +=1
            j += 1
            phase -= 1
        else:
            i -=1
            phase += 1

    aux1 = code_de_Hamming(res[:7])
    aux2 = code_de_Hamming(res[7:])
    aux = aux1 + aux2
    
    return aux

def readEachBlock(m):
    """lecture bloc par bloc"""
    countdown = 0
    n = len(m)-1
    s = len(m)-1
    res = []

    while countdown <= 4:
        res.append(readInBlock(m, n, s))
        res.append(readInBlock(m, n, s-7))
        res.append(readInBlock2(m, n-2, s-13))
        res.append(readInBlock2(m, n-2, s-6))
        n -= 4
        countdown += 1
    
    res = res[:block_utile(m)]
    return res

def ascii(liste_donnees):
    """Convertion en ascii"""
    table = ''
    for code in liste_donnees:
        cara = conversion_binaire_entier(code)
        table += chr(cara)
    return table

def types_donnees(matrice_image):
    """Choisis entre l'ascii ou l'hexa"""
    donnees_blocks = readEachBlock(matrice_image)
    
    if matrice_image[24][8] == 0:
        sms = hexadecimaux(donnees_blocks)
        return sms
    
    elif matrice_image[24][8] == 1:
        sms = ascii(donnees_blocks)
        return sms

def hexadecimaux(liste_donnees):
    """Conversion de décimal en hexadécimal"""
    liste = []
    liste2 = []
    for i in range(nbrLig(liste_donnees)):
        for j in range(nbrCol(liste_donnees)):
            liste.append(liste_donnees[i][j])
    sms = ""
    decoupee_liste = decoupage46bits(liste, 4)
    for v in decoupee_liste:
        liste2.append(conversion_binaire_entier(v))
    for v in liste2:
        if(v<10):
            sms += str(v)
        if(v == 10):
            sms += "A"
        if(v == 11):
            sms += "B"
        if(v == 12):
            sms += "C"
        if(v == 13):
            sms += "D"
        if(v == 14):
            sms += "E"
        if(v == 15):
            sms += "F"
    return sms

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
    """Applique le bon filtre à la matrice"""
    if QRCode_matrice[22][8] == 0 and QRCode_matrice[23][8] == 0:
        # filtre noire
        return QRCode_matrice
    if QRCode_matrice[22][8] == 0 and QRCode_matrice[23][8] == 1:
        # filte damier
        QRMatrix_avec_filtre = filtre_damier(QRCode_matrice) 
    if QRCode_matrice[22][8] == 1 and QRCode_matrice[23][8] == 0:
        # filtre horizontales
        QRMatrix_avec_filtre = filtre_horizontales(QRCode_matrice) 
    if QRCode_matrice[22][8] == 1 and QRCode_matrice[23][8] == 1:
        # filtre verticales
        QRMatrix_avec_filtre = filtre_verticales(QRCode_matrice) 

    return QRMatrix_avec_filtre


def filtre_damier(QRCode_matrice):
    """Applique le filtre damier au à la matrice du QRcode"""
    b = 0
    for i in range(9, nbrLig(QRCode_matrice)):
        for j in range(11, nbrCol(QRCode_matrice)):
            a = (QRCode_matrice[i][j]) ^ (b % 2)
            QRCode_matrice[i][j] = a
            b += 1
        b += 1

    
    return QRCode_matrice


def filtre_horizontales(QRCode_matrice):
    """Applique le filtre horizontal au à la matrice du QRcode"""
    b = 0
    for i in range(nbrLig(QRCode_matrice)):
        for j in range(nbrCol(QRCode_matrice)):
            if j >= 11 and i >= 9:
                if i % 2 == 1:
                    b = 0
                    QRCode_matrice[i][j] ^= b % 2
                else:
                    b = 1
                    QRCode_matrice[i][j] ^= b % 2       
    return QRCode_matrice


def filtre_verticales(QRCode_matrice):
    """Applique le filtre vertical au à la matrice du QRcode"""
    for i in range(nbrLig(QRCode_matrice)):
        for j in range(nbrCol(QRCode_matrice)):
            if j >= 11 and i >= 9:
                if j % 2 == 1:
                    b = 0
                    QRCode_matrice[i][j] ^= b % 2
                else:
                    b = 1   
                    QRCode_matrice[i][j] ^= b % 2
    return QRCode_matrice


def block_utile(QRCode_matrice):
    """Limite le nombre de bloc utilisé """
    liste = []
    for i in range(13, 18):
        liste.append(QRCode_matrice[i][0])
        nbr_block_utile = conversion_binaire_entier(liste)
    return nbr_block_utile


#fonction utilisé pour tester les codes et bonus
def printBeautifulMatrice(a):
    """affiche une belle matrice"""
    for line in a:
        print('   '.join(map(str, line)))
    



def main(filename):
    """Fonction principale pour lire le qrcode"""
    global QRMatrix
    QRMatrix = loading(filename)
    rotate()
    filtre(QRMatrix)
    print(types_donnees(QRMatrix))


def readQRcode():
    """Fonction pout faciliter les tests de lecture des QRCodes"""
    main("qr_code_damier_ascii.png")
    main("qr_code_ssfiltre_ascii_corrupted.png")
    main("qr_code_ssfiltre_ascii_rotation.png")
    main("qr_code_ssfiltre_ascii.png")
    main("qr_code_ssfiltre_num.png")


readQRcode()



###################################################################################################################################


#Bonus

QRMatrix = [[1 for j in range(25)] for i in range(25)]


def QRSkeleton(m):
    squareInQrcode(m)
    for i in range(6, len(m)-7, 2):
        m[i][6] = 0
        m[6][i] = 0



def squareInQrcode(m):
    """création du squelette de la matrice"""
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


def msgToEncode():
    """Message à convertir en QRCode"""
    return input("")



