################################  TESTS   ########################################
from math import ceil, sqrt

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

import os
import time

from Graphe import *
from MethodesApprochees import *
from SeparationEvaluation import *

def dessinerGraphe(tailles, temps, x_label = 'x', y_label='y', title='x en fonction de y', log=False, labels=["Glouton", "Couplage"], nom_fichier='Graphe') :
    
    if isinstance(temps, np.ndarray):
        for i in range(len(temps)):
            plt.plot(tailles, temps[i], label = labels[i])
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.legend()
    else:
        plt.plot(tailles, temps, label =labels)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.legend()

    plt.title(title)

    # vérifier si le dossier "plots" existe, sinon le créer
    if not os.path.exists("plots"):
        os.makedirs("plots")
    
    # enregistrer le graphe
    chemin= 'plots/'
    plt.savefig(chemin + nom_fichier + '.png')
    
    plt.show()
    


def dessinerGraphe3D(n_values, p_values, fonction, evaluation='T'): 
    """
    evaluation est le paramètre qui definit si on veut dessiner un graphe 3d pour évaluer 
    le temps 'T' ou la qualité 'Q' de la solution de l'algorithme donné en entrée 
    
    """
    # créer des grilles 2D pour n et p
    n, p = np.meshgrid(n_values, p_values)

    # créer un tableau pour stocker les temps d'exécution (resp. taille couplage)
    resutat_evaluation = np.zeros_like(n, dtype=float)

    # executer l'algorithme pour différentes combinaisons de n et p
    for n_i in range(len(n_values)):
        for p_j in range(len(p_values)):
            
            nbGraphesGeneres=5
            
            if(evaluation=='T'): #evaluer par rapport au temps 
                
                times =  np.zeros((nbGraphesGeneres))   #times va contenir les temps de chaque iteration 

                for r in range(nbGraphesGeneres):              #Calcule le temps d'execution de la fonction sur plusieurs graphes de meme taille

                    G = genererGraphe(int(n_values[n_i]), p_values[p_j])     #Generer un graphe de taille n=n_values[n_i] et avec une probabilite p=p_values[p_j]

                    start = time.time()         #calculer le temps d'execution pour l'instance donnee
                    c = fonction(G)
                    end = time.time()
                    times[r] = (end-start)

                temps_moyen=np.mean(list(times))  #calculer la moyenne des temps d'execution pour les graphes de taille j et l'ajouter au vecteur des moyennes

                resutat_evaluation[p_j][n_i] = float(temps_moyen)
                
            elif (evaluation=='Q'): #evaluer par rapport à la qualité de la solution (taille couplage)
                
                tailleCouverture =  np.zeros((nbGraphesGeneres))   #va contenir les tailles de couverture retournées à chaque iteration 
                for r in range(nbGraphesGeneres):              #Calcule le temps d'execution de la fonction sur plusieurs graphes de meme taille
                    G = genererGraphe(int(n_values[n_i]), p_values[p_j])     #Generer un graphe de taille n=n_values[n_i] et avec une probabilite p=p_values[p_j]

                    tailleCouverture[r] = len(fonction(G))             #Calculer la taille d la solution retournée par la fonction 
            

                tailleCouv_moyenne=np.mean(list(tailleCouverture))  #calculer la moyenne des temps d'execution pour les graphes de taille j et l'ajouter au vecteur des moyennes

                resutat_evaluation[p_j][n_i] = float(tailleCouv_moyenne)
            
        
    #creer le graphique 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #afficher la surface 3D
    ax.plot_surface(n, p, resutat_evaluation)

    # Ajoutez des étiquettes aux axes
    ax.set_xlabel('n')
    ax.set_ylabel('p')
    
    # vérifier si le dossier "plots" existe, sinon le créer
    if not os.path.exists("plots"):
        os.makedirs("plots")
    
    # enregistrer le graphe
    chemin= 'plots/'
    
    if(evaluation=='T'):
        ax.set_zlabel('Temps d\'exécution (s)')
        
        if(fonction==algo_couplage):
            nom_fichier="3D_temps_couplage"
            plt.title('Evolution du temps d\'exécution de Couplage en fonction de n et p')
        
        elif(fonction==algo_glouton):
            nom_fichier="3D_temps_glouton"
            plt.title('Evolution du temps d\'exécution de Glouton en fonction de n et p')
        
         
    elif (evaluation=='Q') :
        ax.set_zlabel('Taille couverture')
        
        if(fonction==algo_couplage):
            nom_fichier="3D_qualite_couplage"
            plt.title('Taille de la couverture de Couplage en fonction de n et p')
        
        elif(fonction==algo_glouton):
            nom_fichier="3D_qualite_glouton"
            plt.title('Taille de la couverture de Glouton en fonction de n et p')
        
         
        
    plt.savefig(chemin + nom_fichier + '.png')
    plt.show()

    
    
def calculerTemps(fonction, tailles, p, n):#, p
    times =  np.zeros((n))   #times va contenir les temps de chaque iteration 
    means = []               #va contenir les moyennes des temps pour des instances de tailles allant de 2 a m

    for j in tailles:
        for i in range(n):              #Calcule le temps d'execution de la fonction sur plusieurs graphes de meme taille
            if p == -1:
                p=1/sqrt(j)
                
            G = genererGraphe(j, p)     #Generer un graphe de taille j et avec une probabilite p

            start = time.time()         #calculer le temps d'execution pour l'instance donnee
            c = fonction(G)
            end = time.time()
            times[i] = end-start

        means.append(np.mean(list(times)))  #calculer la moyenne des temps d'execution pour les graphes de taille j et l'ajouter au vecteur des moyennes

    return means


def calculerTailleCouverture(fonction, tailles, p, n):#, p
    tailleCouverture =  np.zeros((n))   #va contenir les tailles de couverture retournées à chaque iteration
    means = []               #va contenir les moyennes des temps pour des instances de tailles allant de 2 a m

    for j in tailles:
        for i in range(n):              #Calcule le temps d'execution de la fonction sur plusieurs graphes de meme taille
            if p == -1:
                p=1/sqrt(j)
            G = genererGraphe(j, p)     #Generer un graphe de taille j et avec une probabilite p

                     
            tailleCouverture[i] = len(fonction(G))             #Calculer la taille d la solution retournée par la fonction 
            
        means.append(np.mean(list(tailleCouverture)))  #calculer la moyenne des tailles de couverture pour les graphes de taille j et l'ajouter au vecteur des moyennes

    return means

 

def calculerNbNoeuds(fonction, tailles, p, n):#, p
    nbNoeuds =  np.zeros((n))   #va contenir le nombre de noeuds générés à chaque iteration 
    means = []               #va contenir les moyennes des temps pour des instances de tailles allant de 2 a m

    for j in tailles:
        for i in range(n):              #Calcule le temps d'execution de la fonction sur plusieurs graphes de meme taille
            if p == -1:
                p=1/sqrt(j)
            G = genererGraphe(j, p)     #Generer un graphe de taille j et avec une probabilite p

                     
            c, nbNoeuds[i] = fonction(G, True)             #enregistrer le nombre de noeuds retournée par la fonction 
           
        means.append(np.mean(list(nbNoeuds)))  #calculer la moyenne du nombre de noeuds pour les graphes de taille j et l'ajouter au vecteur des moyennes

    return means

 

    
def calculerComplexiteExpo(tailles, temps):
    #x_log = np.log(np.array([float(t) for t in tailles]))
    x = np.array([float(t) for t in tailles])
    y= np.log(temps)#[0]

    # Approximation par une droite
    coeffs = np.polyfit(x, y, 1)
    a, b = coeffs
    y_pred = a*x + b
    
    # Tracé de la courbe originale et de la droite d'approximation
    plt.plot(x, y, label='Courbe originale')
    plt.plot(x, y_pred, label='Droite d\'approximation')
    plt.legend()
    plt.show()
    print(f"complexite en O({(np.round(np.exp(a),2))}**x)")

    
def calculerComplexitePoly(tailles, temps):
    #x_log = np.log(np.array([float(t) for t in tailles]))
    x = np.log(np.array([float(t) for t in tailles]))
    y= np.log(temps)#[0]

    # Approximation par une droite
    coeffs = np.polyfit(x, y, 1)
    a, b = coeffs
    y_pred = a*x + b
    
    # Tracé de la courbe originale et de la droite d'approximation
    plt.plot(x, y, label='Courbe originale')
    plt.plot(x, y_pred, label='Droite d\'approximation')
    plt.legend()
    plt.show()
    print(f"complexite en O(n**{np.round(a,2)}))")
    

    


def sauvegarderDonnes(nom_fichier, x, y):
    
    # vérifier si le dossier "data" existe, sinon le créer
    if not os.path.exists("data"):
        os.makedirs("data")

    #enregistrer les données dans un fichier pickel
    chemin_data= 'data/'
    name=chemin_data + nom_fichier
    with open(name+'.pickle', 'wb') as fichier_pickle:
        pickle.dump({'x': x, 'y': y}, fichier_pickle)
    

def lireDonnes(name):
    with open(name+'.pickle', 'rb') as fichier_pickle:
        return (pickle.load(fichier_pickle))


 

def calculerRapportApproximation(fonction, tailles, p, n):#, p
    tailleCouverture_Approchee = np.zeros((n))   #va contenir les tailles de couverture retournées par les algos approchés (couplage et glouton) à chaque iteration 
    
    tailleCouverture_Exacte = np.zeros((n)) #va contenir les tailles de couverture retournées par un algorithme exacte (branchement_ameliore_maxDeg) à chaque iteration 

    rapports_moyens = []               #va contenir les moyennes des rapport d'approximation

    for j in tailles:
        for i in range(n):              #Calcule le temps d'execution de la fonction sur plusieurs graphes de meme taille
            if p == -1:
                p=1/sqrt(j)
            G = genererGraphe(j, p)     #Generer un graphe de taille j et avec une probabilite p
            sommets=frozenset(G[1])
            G_ = G.copy()
                        
            tailleCouverture_Approchee[i] = len(fonction(G))             #Calculer la taille de la solution retournée par la fonction 
            
            G_[1]=sommets
            tailleCouverture_Exacte[i] = len(branchement_ameliore_maxDeg(G_))

        rapports_moyens.append(np.mean(list(tailleCouverture_Approchee))/np.mean(list(tailleCouverture_Exacte)))  #calculer la moyenne des tailles de couverture pour les graphes de taille j et l'ajouter au vecteur des moyennes

    return rapports_moyens    
  