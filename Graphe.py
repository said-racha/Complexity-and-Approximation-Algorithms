################################  GRAPHES   ########################################

import random as rd

#Notre structure de graphe se presente sous la forme d'une liste de 4 elements, comme suit :
#le premier: le nombre de sommets,
#le deuxieme: un set des sommets du graphe
#le troisieme: le nombre d'aretes du graphe
#le quatrieme: un set des aretes du graphe, ou chaque arete est un tuple (sommet1, sommet2)

#Voici le graphe associe au fichier exempleinstance.txt: 
#[5, {0, 1, 2, 3, 4}, 6, {(0, 1), (1, 2), (0, 3), (4, 2), (3, 2), (4, 1)}]

#Contraintes sur les graphes:
#Il ne peut pas y avoir d'aretes identiques (une seule parmi les aretes (1,2) et (2,1) sera prise)
#Le graphe doit contenir a tout moment au moins un sommet


# Cette fonction construit un graphe a partir d'un fichier structure comme le fichier "exempleinstance.txt" donne
def lireGraphe(fichier):
  with open(fichier, "r") as f:
    G = []   #Le graphe est une liste dont le premier element est le nombre de sommets, le second représente la liste de ses sommets, le 3e le nombre de ses arètes, le 4e une liste contenant les arètes sous forme de tuples de sommets
    Lines = f.readlines()


  def lireNbSommets():
    nbSommets = Lines[1][:-1] #lire le nombre de sommets et [:-1] sert à supprimer le caractere de saut de ligne '\n'
    G.append(int(nbSommets))

  def lireSommets():
    sommets = []

    for line in Lines[3:3+G[0]]: #commencer à lire à partir du premier sommet jusqu'au dernier soit sauter les 3 premieres lignes et lire jusqu'a atteindre le nombre de sommets défini
      sommets.append(int(line[:-1]))

    G.append(set(sommets)) #convertir la liste en set pour eviter les doublons

  def lireNbAretes():
    nbAretes = Lines[3+G[0]+1][:-1]
    G.append(int(nbAretes))

  def lireAretes():
    aretes = []

    for line in Lines[3+G[0]+3:]:
      indice_espace=line.index(' ') #repérer l'indice du séparateur entre les deux sommets qui définissent un arc
      sommet1 = int(line[0:indice_espace]) #lire le premier sommet
      sommet2 = int(line[indice_espace+1:-1])  #lire le deuxième sommet

      arete = (sommet1, sommet2)
      if (sommet2, sommet1) not in aretes: #verifier que l'arete n'a pas été deja introduite avec un sens inverse des sommets
        aretes.append(arete)

    G.append(set(aretes)) #set permet de s'assurer de ne pas avoir de doublons

  lireNbSommets()
  lireSommets()
  lireNbAretes()
  lireAretes()

  return G

#Cette fonction retourne les voisins d'un sommet donne dans un graphe G (les sommets qui partagent une arete avec lui)
def getVoisins(G,sommet):
  E=G[3]
  voisins=[]
  for i,j in E :
    if i==sommet:
      voisins.append(j)
    elif j==sommet:
      voisins.append(i)
  return set(voisins)

######## 2.1 OPERATIONS DE BASE 
##Q2.1.1
def supprimerSommet(G_init,v):
  G=G_init.copy()
  if G[0]>1 : #s'assurer que G comporte au moins deux sommets (on considère qu'un graphe doit garder au moins un sommet)
    if(v in G[1]): #on ne peut supprimer une arete que si elle existe dans G
      G[1].remove(v) #supprimer le sommet de la liste des sommets
      G[0] -=1 #mettre à jour le nombre de sommets de G

      #supprimer toutes les aretes pour lesquelles v est une
      aretes=G[3].copy() #créer une copie afin d'éviter de supprimer sur une liste qu'on itère
      for arete in G[3]:
        if v in arete :
          aretes.remove(arete) #supprimer l'arete de l'ensemble des aretes de G
          G[2] -=1 #mettre à jour le  nombre d'aretes de G
      G[3]=aretes.copy()
    else:
      raise Exception("Le sommet que vous souhaitez supprimer n'existe pas dans le graphe")
  else:
      raise Exception("Un graphe doit contenir au moins un sommet")
  return G

##Q2.1.2
def supprimerNSommets(G_init,list_v):
  G=G_init.copy()
  for v in list_v:
    G=supprimerSommet(G,v)
  return G

##Q2.1.3
def getDegres (G): #retourne un tableau de tuple tel que chaque sommet et associé à son degré
  degres=[]

  for sommet in G[1]: #parcourir tous les sommets de G
    degre=0
    for arete in G[3]: #compter le nombre de fois ou chaque sommet apparait en tant qu'extrémité d'une arete
      if sommet in arete :
        degre +=1
    degres.append((sommet, degre)) #créer un tuple pour représenté le degré de chaque sommet de G

  return degres

#CAS 1 : retourne un sommet de degré max
def getMaxDegre (G):
  degres=getDegres(G) #recuperer le tableau contenant les degrés des sommets de G
  #initialiser les variables
  max=-1
  sommet_max=-1
  #parcourir les tuples du tableau de sorte à ressortir le premier sommet de degré max
  for tuple in degres:
    if tuple[1]>max:
      max=tuple[1]
      sommet_max=tuple[0]
  return sommet_max

#CAS 2 : retourne une liste de sommet de degré max
def getListMaxDegre (G):
  degres=getDegres(G) #recuperer le tableau contenant les degrés des sommets de G
  #initialiser les variables
  max=-1
  sommet_max=[]

  #parcourir les tuples du tableau de sorte à ressortir le degré max de G
  for tuple in degres:
    if tuple[1]>max:
      max=tuple[1]
  #parcourir les tuples du tableau de sorte à ressortir tous les sommets de degré max dans G
  for tuple in degres:
    if tuple[1]==max:
      sommet_max.append(tuple[0])

  return sommet_max


######## 2.1 OPERATIONS DE BASE 
##Q2.2.1
def genererGraphe (n,p):
  #verifier que n est un entier positif et p une proba entre 0 et 1
  if(n<0 or not isinstance(n,int)):
    raise Exception("Le premier paramètre 'n' doit etre un entier positif")
  if(p<=0 or p>=1):
    raise Exception("Le deuxième paramètre 'p' doit etre une valeur de probabilité entre 0 et 1")

  G=[0,set(),0,set()]
  for i in range(n):
    for j in range(n):
      if(i!=j): #une arete doit etre composée à partir de deux sommets distincts

        if(rd.random()<=p): #créer une arete entre i et j avec une probabilité de p
          #ajouter i et j à la liste des sommets de G
          G[1].add(i)
          G[1].add(j)
          G[0]=len(G[1]) #compter le nombre de sommets de G (dans un set)

          aretes=G[3].copy()
          if (j, i) not in G[3]: #verifier que l'arete n'a pas été deja introduite avec un sens inverse des sommets
            aretes.add((i,j)) #ajouter l'arete (i,j) à la liste des aretes de G
          G[3]=aretes.copy()
          G[2]=len(G[3]) #compter le nombre d'aretes de G (dans un set)

  while(G[2]==0): #s'assurer que le graphe à retourner n'est pas vide
    G=genererGraphe(n,p)

  return G




