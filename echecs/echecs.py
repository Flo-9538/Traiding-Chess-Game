#-------------------------------------------------------------------------------------jeu d'échec----------------------------------------------------------------------------------------------


#-------------------------préambule------------------------------

""" Voici mon programme de jeu d'echec, il peut être joué, pour l'instant par 2 joueurs sur le même PC, dans le terminal python, quand c'est son tour, le joueur choisi les coordonnées d'une pièce à déplacer, et ses nouvelle coordonné (co normal des echecs), affichages se fait également dans le terminal grace aux émojis du jeu d'échec."""


#------------------------import de fonctions-------------------------

import numpy as np
import pygame
import sys
import time

#-------------------correspondance valeurs-symboles ------------------------

dict_valeurs_symbole={
    "nP":"♟", 
    "nT":"♜",
    "nC":"♞",
    "nF":"♝",
    "nD":"♛",
    "nR":"♚",

    "bT":"♖",
    "bC":"♘",
    "bF":"♗",
    "bD":"♕",
    "bR":"♔",
    "bP":"♙",

    "vV":"▢"
}

fin=False

#-------------- création plateau et echequier----------------

colonnes=["a","b","c","d","e","f","g","h"]
lignes=["8","7","6","5","4","3","2","1"]

plateau_coord_alg=np.full((8, 8), "xx", dtype=object) 
#print(plateau_coord_alg)

for i in range (0,8):
    for j in range (0,8):
        plateau_coord_alg[i][j]=colonnes[j]+lignes[i] # matrice des coordonnés algébrique

print(plateau_coord_alg)

echequier=np.full((8, 8), "x", dtype=object)


#------------------------------transformer une coord algébrique en coordonnés de matrice-----------------------------------

def alg_to_co(coord_alg): # permet la transformation de coordonnés algébriques en coordonnés plateau on ne s'interesse pas à la valeur
    ligne=-1
    colonne=-1
    for i in range (0,8):
        if ["a","b","c","d","e","f","g","h"][i]==coord_alg[0]:
            colonne=i
    for i in range (0,8):
        if ["8","7","6","5","4","3","2","1"][i]==coord_alg[1]:
            ligne=i
    return (ligne,colonne)


# -------------------------------------pour chercher une liste de pièces sur l'echequier-------------------------

def recherche(echequier,valeur): # permet la transformation de coordonnés algébriques en coordonnés plateau on ne s'interesse pas à la valeur
    co=[] # tuple de co qui sert à chercher une pièce sur l'échequier
    for lig in range (0,8):
        for col in range (0,8):
            if echequier[lig][col]==valeur:
                co.append((lig,col))
    return co


#---------------------------------------pour attribier une valeur à une case de l'echequier-------------------------------------

def attribution(jose,coordonnees,new_valeur): #jose=echequier
    (i,j)=coordonnees
    jose[i][j]=new_valeur
    return jose

#---------------------------------------affichage terminal----------------------------------------

def affichage1(echequier,dict_valeurs_symbole):
    print("  "+" ".join(["a","b","c","d","e","f","g","h"][colonne]+" " for colonne in range(0,8)))
    for ligne in range(0,8):        
        print(["8","7","6","5","4","3","2","1"][ligne]+" "+" ".join(dict_valeurs_symbole[echequier[ligne][colonne]]+" " for colonne in range(0,8)))

#-----------------------------------placement initial sur l'echequier--------------------------------------

def placement_initial(plateau_coord_alg,echequier):
    for ligne in range(0,8):
        for colonne in range(0,8):

            coordonnées=plateau_coord_alg[ligne][colonne]

            valeur="vV" #valeur de base (vide)

            #noir
            if coordonnées=="a8" or coordonnées=="h8":
                valeur="nT"
            if coordonnées=="b8" or coordonnées=="g8":
                valeur="nC"
            if coordonnées=="c8" or coordonnées=="f8":
                valeur="nF"
            if coordonnées=="d8":
                valeur="nD"
            if coordonnées=="e8":
                valeur="nR"
            if coordonnées[1]=="7":
                valeur="nP"

            #blanc
            
            if coordonnées=="a1" or coordonnées=="h1":
                valeur="bT"
            if coordonnées=="b1" or coordonnées=="g1":
                valeur="bC"
            if coordonnées=="c1" or coordonnées=="f1":
                valeur="bF"
            if coordonnées=="d1":
                valeur="bD"""
            if coordonnées=="e1":
                valeur="bR"                
            if coordonnées[1]=="2":
                valeur="bP"

            echequier[ligne][colonne]=valeur

    return(echequier)


#------------------------------------deplacement pion------------------------------------------

def dep_pion(pre_co,new_co,echequier,en_passant,promotion,valeur_depart,valeur_arrive):

    (pre_lig,pre_col)=pre_co
    (new_lig,new_col)=new_co
    verif=False

    if valeur_depart=="bP": # c'est un pion blanc qui se déplace
        if pre_lig==6 and new_lig==4 and pre_col==new_col : #il est en x2 il va en x4
            if echequier[5][pre_lig]=="vV" and echequier[4][pre_lig]=="vV": #si rien ne le bloque
                verif=True
                en_passant[0]=new_co #coord de la pièce qui peut être prise en passant
        if new_lig==pre_lig-1 and pre_col==new_col and echequier[new_lig][new_col]=="vV": # si le pion avance de 1 et que l'arrivé est vide
            verif=True
        if new_lig==pre_lig-1 and (new_col==pre_col+1 or new_col==pre_col-1): #si on se décale d'une colonne et qu'un avance d'une ligne
            if valeur_arrive!="vV": # si l'arrivé est mangeable
                verif=True
            if en_passant[2][0]==pre_lig and en_passant[2][1]==new_col and new_lig==pre_lig-1 and valeur_arrive=="vV": #si on peut prendre en passant (ligne de départ = ligne de en-passant et colonne d'arrivé = colonne de en passant) et on avance d'une case et la case d'arrivé est vide
                verif=True
                en_passant[3]=True
        if new_lig==0 and verif==True:
                promotion=new_co

    if valeur_depart=="nP": # c'est un pion noir qui se déplace

        if pre_lig==1 and new_lig==3 and pre_col==new_col: #il est en x7 il va en x5
            if echequier[2][pre_col]=="vV" and echequier[3][pre_col]=="vV": #si rien ne le bloque
                verif=True
                en_passant[2]=new_co #coord de la pièce qui peut être prise en passant
        if new_lig==pre_lig+1 and pre_col==new_col and echequier[new_lig][new_col]=="vV": # si le pion avance de 1 et que l'arrivé est vide
            verif=True
        if new_lig==pre_lig+1 and (new_col==pre_col+1 or new_col==pre_col-1): #si on se décale d'une colonne et qu'un avance d'une ligne
            if valeur_arrive!="vV":
                verif=True
                #print("Pl")
            if en_passant[0][0]==pre_lig and en_passant[0][1]==new_col and new_lig==pre_lig+1 and valeur_arrive=="vV": #si on peut prendre en passant (ligne de départ = ligne de en-passant et colonne d'arrivé = colonne de en passant) et on avance d'une case et la case d'arrivé est vide
                verif=True
                en_passant[1]=True
        if new_lig==7 and verif==True:
            promotion=new_co
        #print("deppion",pre_co,new_co,valeur_depart,valeur_arrive)

    return(verif,en_passant,promotion)


#-----------------------------------déplacement tour--------------------------------------------

def dep_tour(pre_co,new_co,echequier):

    (pre_lig,pre_col)=pre_co
    (new_lig,new_col)=new_co
    nb_piece=0
    verif=False

    if new_col==pre_col: #déplacement vertical
        if new_lig>pre_lig:                
            for lig in range(pre_lig+1,new_lig): #on répète le nombre de ligne
                if echequier[lig][pre_col]!="vV":
                    nb_piece+=1 #on compte le nb de piece entre depart et arrivé
        if new_lig<pre_lig:
            for lig in range(new_lig+1,pre_lig): #on répète le nombre de ligne
                if echequier[lig][pre_col]!="vV":
                    nb_piece+=1 #on compte le nb de piece entre depart et arrivé
        if nb_piece==0:
            verif=True #si il y a rien c'est true

    if new_lig==pre_lig: #déplacement horizontal
        if new_col>pre_col:
            for col in range(pre_col+1,new_col):                  
                if echequier[pre_lig][col]!="vV":
                    nb_piece+=1 
        if new_col<pre_col:
            for col in range(new_col+1,pre_col):                  
                if echequier[pre_lig][col]!="vV":
                    nb_piece+=1                     
    
        if nb_piece==0:
            verif=True #si il y a rien c'est true

    return verif


#------------------------------------déplacement fou----------------------------------------------

def dep_fou(pre_co,new_co,echequier):

    (pre_lig,pre_col)=pre_co
    (new_lig,new_col)=new_co
    nb_piece=0
    verif=False

    for n in range (1,8): #on peut se déplacer de 1 à 7 cases
        if (pre_lig+n==new_lig and pre_col+n==new_col): #bas droite
            for k in range (1,n):
                if echequier[pre_lig+k][pre_col+k]!="vV": #on répète en ajoutant ou enlevant à chaque fois i ligne ou une colonne en fonction de la direction
                    nb_piece+=1 #on ajoute 1 si il y a une pièce
            if nb_piece==0:
                verif=True #si il n'y en a pas verif=True
        if (pre_lig+n==new_lig and pre_col-n==new_col): #bas gauche
            for k in range (1,n):
                if echequier[pre_lig+k][pre_col-k]!="vV":
                    nb_piece+=1 
            if nb_piece==0:
                verif=True
        if (pre_lig-n==new_lig and pre_col+n==new_col): #haut droite
            for k in range (1,n):
                if echequier[pre_lig-k][pre_col+k]!="vV":
                    nb_piece+=1 
            if nb_piece==0:
                verif=True
        if (pre_lig-n==new_lig and pre_col-n==new_col): #haut gauche
            for k in range (1,n):
                if echequier[pre_lig-k][pre_col-k]!="vV":
                    nb_piece+=1
            if nb_piece==0:
                verif=True

    return verif


#------------------------déplacement cavalier-------------------------------

def dep_cav(pre_co,new_co,echequier):

    (pre_lig,pre_col)=pre_co
    (new_lig,new_col)=new_co
    verif=False

    if ((new_col==pre_col-2 or new_col==pre_col+2) and (new_lig==pre_lig+1 or new_lig==pre_lig-1)) or ((new_col==pre_col-1 or new_col==pre_col+1) and (new_lig==pre_lig+2 or new_lig==pre_lig-2)): #8 déplacement possibles
        verif=True

    return verif


#----------------------déplacement dame----------------------------

def dep_dame(pre_co,new_co,echequier): #dep_tour,dep_fou

    verif_T=dep_fou(pre_co,new_co,echequier)
    verif_F=dep_tour(pre_co,new_co,echequier)

    if verif_T==True or verif_F==True:
        verif=True
    else:
        verif=False

    return verif


#-----------------------déplacement roi--------------------------

def dep_roi(pre_co,new_co,echequier,roque):

    (pre_lig,pre_col)=pre_co
    (new_lig,new_col)=new_co
    verif=False
                    
    if (pre_lig==new_lig and (new_col==pre_col+1 or new_col==pre_col-1)) or (pre_col==new_col and (new_lig==pre_lig+1 or new_lig==pre_lig-1)) or (pre_lig==new_lig+1 and pre_col==new_col+1) or (pre_lig==new_lig-1 and pre_col==new_col+1) or (pre_lig==new_lig+1 and pre_col==new_col-1) or (pre_lig==new_lig-1 and pre_col==new_col-1): #on se déplace d'une case (y a certainement plus simple mais bon)
        verif=True

    #print(roque)

    if roque[0]=="possible" and echequier[0][1]=="vV" and echequier[0][2]=="vV" and echequier[0][3]=="vV" and new_co==(0,2):
        verif=True
        roque[0]="actif"

    if roque[1]=="possible" and echequier[0][5]=="vV" and echequier[0][6]=="vV" and new_co==(0,6):
        verif=True
        roque[1]="actif"

    if roque[2]=="possible" and echequier[7][1]=="vV" and echequier[7][2]=="vV" and echequier[7][3]=="vV" and new_co==(7,2):
        verif=True
        roque[2]="actif"        

    if roque[3]=="possible" and echequier[7][5]=="vV" and echequier[7][6]=="vV" and new_co==(7,6):
        verif=True
        roque[3]="actif"
        print(roque,"3")

    return (verif,roque) # si le coup est possible, alors on retourn verif=True, il sera alors joué, donc on met à jour le roque




#--------------------------------vérification d'un coup (utilise la vérification d'échec)-------------------------------------------

# le vérification à pour but de vérifier si le coup joué est valide ainsi que le roque et la promotion

def verification(echequier,pre_co,new_co,roque,tour,en_passant):  # rappel: co[0]=ligne co[1]=colonne    

    verif=False #la vérification est d'abors fausse, elle le restera si aucuns des if n'est vérifié, le coup ne peut pas être joué. Sinon elle deviendra vrai
    promotion=(-1,-1) #la promotion n'est pas activé, elle le sera si les conditions sont vérifiés
    nb_piece=0 #le nb de pièce entre le départ et l'arrivé est initialement à 0

    (pre_lig,pre_col)=pre_co
    (new_lig,new_col)=new_co
    valeur_depart=echequier[pre_lig][pre_col]
    valeur_arrive=echequier[new_lig][new_col]

    #print(valeur_depart,pre_lig,pre_col)
    #print(valeur_arrive,new_lig,new_col)

    echequier_suppose=echequier.copy()
    echequier_suppose=attribution(echequier_suppose,pre_co,"vV")
    echequier_suppose=attribution(echequier_suppose,new_co,valeur_depart)

    echec=verif_echec(echequier_suppose,tour)

    if echec==0:

        if valeur_depart[0]==tour[0] and valeur_arrive[1]!="R": #si le pion choisis correspond au tour du joueur et que c'est pas le roi qui est graille

            (verif,en_passant,promotion)=dep_pion(pre_co,new_co,echequier,en_passant,promotion,valeur_depart,valeur_arrive)

            if valeur_arrive[1]!="R" and valeur_arrive[0]!=tour[0] : #si on mange pas le roi et si on ne mange pas un pion de la même couleur

                if valeur_depart[1]=="T":               
                    verif=dep_tour(pre_co,new_co,echequier)

                if valeur_depart[1]=="F":
                    verif=dep_fou(pre_co,new_co,echequier)

                if valeur_depart[1]=="C": 
                    verif=dep_cav(pre_co,new_co,echequier)

                if valeur_depart[1]=="D":
                    verif=dep_dame(pre_co,new_co,echequier)

                if valeur_depart[1]=="R":
                    (verif,roque)=dep_roi(pre_co,new_co,echequier,roque)

    return (verif,roque,promotion,en_passant)


#-------------------------------------fonction de vérification d'échec------------------------------------------

def verif_echec(echequier,couleur):

    #print(echequier,"verif_echec")

    roi_co=recherche(echequier,couleur[0]+"R")[0] #recherche du roi en fonction de la couleur recherché, si couleur blanche, on cherche si le roi blanc est en echec

    echec=0 #si l'une des pièce peut manger le roi, echec=True

    for ligne in range(0,8): # pour chaque pièce, on regarde si elle peut manger le roi
        for colonne in range(0,8):

            valeur_depart=echequier[ligne][colonne]

            pre_co=(ligne,colonne)

            if valeur_depart[0]!=couleur[0] and valeur_depart!="vV": # si la couleur de la valeur de départ est différente de la couleur du roi et si c'est pas du vide

                #print(valeur_depart,pre_co,roi_co)

                if valeur_depart[1]=="P":
                    if dep_pion(pre_co,roi_co,echequier,[(-1,-1),False,(-1,-1),False],(-1,-1),valeur_depart,couleur[0]+"R")[0]==True: #on peut pas prendre un roi en passant :) la promotion n'a pas d'interet
                        echec+=1
                        #print("Pion echec")

                if valeur_depart[1]=="T":               
                    if dep_tour(pre_co,roi_co,echequier)==True:
                        echec+=1
                        #print("tour echec")

                if valeur_depart[1]=="F":
                    if dep_fou(pre_co,roi_co,echequier)==True:
                        echec+=1
                        #print("fou echec")

                if valeur_depart[1]=="C": 
                    if dep_cav(pre_co,roi_co,echequier)==True:
                        echec+=1
                        #print("cav echec")

                if valeur_depart[1]=="D":
                    if dep_dame(pre_co,roi_co,echequier)==True:
                        echec+=1
                        #print("dame echec")

                if valeur_depart[1]=="R":
                    if dep_roi(pre_co,roi_co,echequier,["interdit","interdit","interdit","interdit"])[0]==True: #on ne peux pas prendre une pièce en roquant
                        echec+=1
                        #print("roi echec")
    #print(echec,"echec")
    return echec


#-------------------------------vérification d'échec et mat-------------------------------

def echec_et_mat(echequier,couleur,roque,en_passant): # on regarde si tel couleur est en echec et mat, pour cela on regarde d'abors si le roi est en echec, si oui, on prend chaques pièce une par une, et on les faits se déplacer sur toutes les cases de l'échequier, si elle peuvent se déplacer, et que le roi n'est plus en echec, il n'y a pas d'echec et mat.
    liberation_possible=False
    echecetmat=True
    it=0
    roi_co=recherche(echequier,couleur[0]+"R")[0]
    for pre_lig in range(0,8):
        for pre_col in range(0,8):
            if echequier[pre_lig][pre_col][0]==couleur[0]: #si c'est bien la couleur dont on veut savoir qu'elle est en echec et mat
                for new_lig in range(0,8):
                    for new_col in range(0,8):
                        if roi_co!=(new_lig,new_col):
                            verif_coup=verification(echequier,(pre_lig,pre_col),(new_lig,new_col),roque,couleur,en_passant)[0] #si verif == True, ça veut dire que que la pièce peut bien bouger et que le roi n'est plus en echec, le roque et la prise en passant peuvent débloquer une situation d'échec
                            if verif_coup==True:
                                liberation_possible=True
                            #print(echequier,(pre_col,pre_lig),(new_lig,new_col),"echec et mat")
                            #print(liberation_possible)
                            it+=1
    #print(it)
    if liberation_possible==True:
        echecetmat=False
    return echecetmat


#------------------------------roque-----------------------------------------

def roque_(roque,echequier,pre_coord_alg): # si le roque est effectué, il y a un déplacement de plus à faire pour la tour

    #print(roque,"2") #l'un des roque n'est pas actif

    if roque[3]=="actif": #on déplace la tour blanche grace au roque
        echequier=attribution(echequier,alg_to_co("h1"),"vV") 
        echequier=attribution(echequier,alg_to_co("f1"),"bT")

    if roque[2]=="actif":
        echequier=attribution(echequier,alg_to_co("a1"),"vV") 
        echequier=attribution(echequier,alg_to_co("d1"),"bT")

    if roque[1]=="actif": #on déplace la tour noir grace au roque
        echequier=attribution(echequier,alg_to_co("h8"),"vV") 
        echequier=attribution(echequier,alg_to_co("f8"),"nT")

    if roque[0]=="actif":
        echequier=attribution(echequier,alg_to_co("a8"),"vV") 
        echequier=attribution(echequier,alg_to_co("d8"),"nT")

    # on met à jour les conditions du roque

    if pre_coord_alg=="a8" or pre_coord_alg=="e8":
        roque[0]="interdit"
    if pre_coord_alg=="h8" or pre_coord_alg=="e8":
        roque[1]="interdit"
    if pre_coord_alg=="a1" or pre_coord_alg=="e1":
        roque[2]="interdit"
    if pre_coord_alg=="h1" or pre_coord_alg=="e1":
        roque[3]="interdit"

    return(echequier,roque)    


#-----------------------------promotion (uniquement terminal)-------------------------------

def promotion_(promotion,echequier,tour):#on écrit la promotion comme une coord: "f8", ce qui indique la couleur la case
    #print("promotion activé")
    if promotion[0]==7 or promotion[0]==0: 
        new_valeur_prom=str(input("Choisir une promotion (Tour=T, Cavalier=V, Fou=F, Dame=D) : "))
        echequier=attribution(echequier,promotion,tour[0]+new_valeur_prom) 
    #print(promotion)
    return(echequier)


#--------------------------------prise en passant-------------------------------

def en_passant_(en_passant,echequier): #si il y a une prise en passant, on remplace la pièce prise par du vide
    if en_passant[1]==True:
        echequier=attribution(echequier,en_passant[0],"vV") 
    if en_passant[3]==True:
        echequier=attribution(echequier,en_passant[2],"vV")
    return echequier





# Couleurs
blanc = (255, 255, 255)
beige=(242, 225, 241)
vert=(118, 198, 71)
noir = (0, 0, 0)
gris_clair = (200, 200, 200)

# Échiquier : une matrice 8x8 (tu peux remplacer par ta propre matrice)
plateau = [[0 for _ in range(8)] for _ in range(8)]

taille_case = 100

echequier=placement_initial(plateau_coord_alg,echequier)


#chargement des pieces
fichier="piece_meme/"
dict_valeurs_images={}
for ligne in range(8):
    for col in range(8):
        piece_image=pygame.image.load(fichier+echequier[ligne][col]+".png")
        piece_image=pygame.transform.scale(piece_image, (taille_case, taille_case))
        dict_valeurs_images[echequier[ligne][col]]=piece_image

# Fonction pour dessiner l'échiquier
def dessiner_plateau(fenetre,echequier):
    
    for ligne in range(8):
        for col in range(8):
            couleur = beige if (ligne + col) % 2 == 0 else vert
            pygame.draw.rect(fenetre, couleur, (col * taille_case, ligne * taille_case, taille_case, taille_case))
            if echequier[ligne][col] != "vV": #affichage des pièces selon les valeurs dans la matrice
                piece_image = dict_valeurs_images[echequier[ligne][col]]
                fenetre.blit(piece_image, (col * taille_case, ligne * taille_case))
                #attention on recharge l'image à chaque fois


def obtenir_case_cliquee(position):
    x, y = position
    col = x // taille_case
    ligne = y // taille_case
    return ligne, col


game_type="c"
#str(input("mode de jeu:\nClassic (pygame): c \nTerminal: t\n"))


def affichage2(echequier,tour):
    print("go")


#----------------------------------corp du programme-----------------------------------------

echequier=placement_initial(plateau_coord_alg,echequier)

affichage1(echequier,dict_valeurs_symbole)

n=0

#les roques sont initialement "possible", ils deviennent "interdit" lorsqu'une pièce à bougé, ils sont "actif" lorsque le roque est activé
roque=["possible","possible","possible","possible"]
#ordre: 
#n_condition_grand_roque  0
#n_condition_petit_roque  1
#b_condition_grand_roque  2
#b_condition_petit_roque  3

en_passant=[(-1,-1),False,(-1,-1),False] #coordonné du pion qui peut être pris en passant, liste [0]=blanc_coord [1]=True=en_passant utilisé par noir, [2]=noir_coord [3]=True=en passant utilisé par blanc

promotion=(-1,-1)



if game_type=="c":
    pygame.init()
    pygame.display.set_caption("Echecs")

    # Paramètres de la fenêtre
    
    fenetre = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Échiquier Cliquable")

    n=1
    tour="blanc"
    select=(-1,-1)
    verif=False
    echmat=False
    selection = pygame.image.load("piece_meme/selection.png")
    selection = pygame.transform.scale(selection, (taille_case, taille_case))
    vide = pygame.image.load("piece_meme/vV.png")
    vide = pygame.transform.scale(vide, (taille_case, taille_case))
    echecetmat = pygame.image.load("piece_meme/EchecEtMat.png")
    echecetmat = pygame.transform.scale(echecetmat, (taille_case*6, taille_case*6))
    dessiner_plateau(fenetre,echequier)

    while True:

        #initialisation du tour
        verif=False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                ligne, col = obtenir_case_cliquee(pos)
                
                if echequier[ligne][col][0]==tour[0]:
                    select=(ligne,col)
                    print("Sélection",select,plateau_coord_alg[ligne][col])
                if select!=(-1,-1) and echequier[ligne][col][0]!=tour[0]:
                    print(f"Déplacement:",select,plateau_coord_alg[ligne][col])
                    new_co=(ligne,col)
                    (verif,roque,promotion,en_passant)=verification(echequier,select,new_co,roque,tour,en_passant) #si verif=false, le reste sera pas modifié (je crois)
                    if verif==True:     
                        print("verif=true")           
                        valeur=echequier[select[0]][select[1]] #valeur de la pièce
                        echequier=attribution(echequier,select,"vV") #on attribue à la case de départ la valeur vide 
                        echequier=attribution(echequier,new_co,valeur) #attribution à la case d'arrivée de la valeur de départ
                        print(echequier)

                        print("roque: ", roque)
                        print("promotion: ",promotion)

                        (echequier,roque)=roque_(roque,echequier,plateau_coord_alg[select[0]][select[1]])
                        echequier=en_passant_(en_passant,echequier)
                        echequier=promotion_(promotion,echequier,tour)

                        affichage1(echequier,dict_valeurs_symbole)

                        select=(-1,-1) #réninitialise selection
                        n+=1 #tour suivant

                        if n%2==1:
                            tour="blanc"
                            en_passant[0]=(-1,-1) #au tour du blanc on reset la possibilité de en passant pour le noir
                            en_passant[1]=False # si True, le blanc c'est fait prendre en passant
                        else:
                            tour="noir"
                            en_passant[2]=(-1,-1)
                            en_passant[3]=False

                        # vérification d'echec et mat pour la couleur du tour actuel
                        if verif_echec(echequier,tour)==True:
                            if echec_et_mat(echequier,tour,roque,en_passant)==True: #si il y a echec et mat
                                print(tour,": Echec et mat, vous avez perdu!")
                                echmat=True        
                        
        dessiner_plateau(fenetre,echequier)
        if select!=(-1,-1):
            fenetre.blit(selection, (select[1] * taille_case, select[0] * taille_case))
        if echmat==True:
            fenetre.blit(echecetmat, (1 * taille_case, 1 * taille_case))
        pygame.display.flip() 


while fin==False:

# valeur du tour blanc ou noir
    n+=1
    if n%2==1:
        tour="blanc"
        en_passant[0]=(-1,-1) #au tour du blanc on reset la possibilité de en passant pour le noir
        en_passant[1]=False # si True, le blanc c'est fait prendre en passant
    else:
        tour="noir"
        en_passant[2]=(-1,-1)
        en_passant[3]=False

    """if echec_et_mat(echequier,tour,roque,en_passant)==True: #avant de jouer on vérifie que le joueur n'est pas en echec et mat (se serait triste)
        print(tour+": echec et mat, vous avez perdu :)")
        fin==True"""

    if verif_echec(echequier,tour)==True:
        if echec_et_mat(echequier,tour,roque,en_passant)==True: #si il y a echec et mat
            fin=True
            print(tour,": Echec et mat, vous avez perdu!")
            break

    pre_coord_alg=str(input(tour+": coordonnées du pion à bouger: "))
    new_coord_alg=str(input(tour+": nouvelles coordonnées du pion: "))

    pre_co=alg_to_co(pre_coord_alg)
    new_co=alg_to_co(new_coord_alg)

    (pre_lig,pre_col)=pre_co
    (new_lig,new_col)=new_co

    if pre_coord_alg=="stop" or new_coord_alg=="stop":
        stop=()
        stop.append(1)

    print(echequier)

    (verif,roque,promotion,en_passant)=verification(echequier,pre_co,new_co,roque,tour,en_passant) #supression plateau coord, remplacement pre_coord par pre_co=(X,X) et new co=(X,X)

    while verif==False:

        print("les coordonnées de départ ou d'arrivé ne sont pas bonnes, changez de coordonnées")
        pre_coord_alg=str(input(tour+": coordonnées du pion à bouger: "))
        new_coord_alg=str(input(tour+": nouvelles coordonnées du pion: "))
        pre_co=alg_to_co(pre_coord_alg)
        new_co=alg_to_co(new_coord_alg)
        (pre_lig,pre_col)=pre_co
        (new_lig,new_col)=new_co
        (verif,roque,promotion,en_passant)=verification(echequier,pre_co,new_co,roque,tour,en_passant)

    valeur=echequier[pre_lig][pre_col] #valeur de la pièce

    print(valeur)

    print(echequier) #j'affiche l'echequier, mais le coup ne devrait pas encore être affiché????? ça n'a pas de sens????

    echequier=attribution(echequier,pre_co,"vV") #on attribue à la case de départ la valeur vide 

    print(echequier)

    echequier=attribution(echequier,new_co,valeur) #attribution à la case d'arrivée de la valeur de départ

    print(echequier)

    #règles spéciales activé grace à la vérification, si un coup spécial est joué, la variable attribué sera modifié, ainsi, il sera possible de modifier l'échequier en conséquence
    (echequier,roque)=roque_(roque,echequier,pre_coord_alg)
    echequier=en_passant_(en_passant,echequier)
    echequier=promotion_(promotion,echequier,tour)

    affichage1(echequier,dict_valeurs_symbole)



# changons le système de coordonnés, les coord sont notés coord_alg pour coordonnés algébrique, sinon, on utilisera un tuple co=(X,X) avec co[0]=lig et co[1]=col

"""Modifications possible: mettre des classes, un truc hors terminal pour la promotion, et peut être une fonction pour les règles de mat et tout ça"""