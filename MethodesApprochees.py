################################  Methodes approchees   ########################################

import random as rd
from Graphe import *

######## 3-Methodes approchees

##Q3.2
def algo_couplage(G):
  #arete_init=tuple(list(G[3])[0])
  aretes = list(G[3].copy())
  rd.shuffle(aretes)

  C=[] #on sait que les arcs dans le graphe sont uniques
  
  def existeDansTuples(tuples, val1, val2): #determine si une parmi val1 et val2 existe dans un des tuples de "tuples"
    if tuples == []:
      return False

    for tuple in tuples:
      if val1 in tuple or val2 in tuple:
        return True
    return False

  for arete in aretes:
    if not existeDansTuples(C, arete[0], arete[1]) :
      C.append(arete)

  return set( [arete[0] for arete in C] + [arete[1] for arete in C])

def algo_glouton(G):
  C=set()
  E=list(G[3].copy())
  rd.shuffle(E) #randomiser
  while len(E)>0: #executer la série d'instructions tant qu'il reste une arete non couverte
    list_sommets_degMax=getListMaxDegre (G) #selectionner les sommets de degrés max de G
    v=list_sommets_degMax[0]
    C.add(v) #ajouter à C un sommet de degré max de G
    G=supprimerSommet(G,v) #supprimer le sommet ajouté précedmeent de G
    E=G[3] #mettre a jour la liste des aretes restantes de G
  return C