################################  Separation et Evaluation   ########################################

from math import ceil, sqrt
import random as rd
from Graphe import *
from MethodesApprochees import algo_couplage

######## 4.1 Branchement 
##Q1.1.1

def branchement(G, getNbNoeuds=False):
                  #getNbNoeuds signifie que l'utilisateur veut connaitre le nombre de noeuds générés par l'algorithme
  nbNoeuds=0
  
  E=list(G[3].copy()) #recuperer l'ensemble des aretes de G
  rd.shuffle(E) #randomiser
  C = set() #initialiser la couverture (la solution a retourner)
  pile=[] #init la pile
  list_sommets_G=frozenset(G[1]) #recuperer l'ensemble des sommets de G

  arete=E[0] #recuperer la premiere arete rencontrée

  sommet1=arete[0] #recuperer le premier sommet de l'arete
  sommet2=arete[1] #recuperer le deuxieme sommet de l'arete

  #empiler les deux premiers sommets et la solution à l'état initial
  pile.append((sommet1, C.copy()))
  pile.append((sommet2, C.copy()))
  #Note : sommet2 est choisit dans la solution courante car sommet2 est au sommet de la pile

  #incrémenter de 2 le nombre de noeuds générés par le branchement
  if(getNbNoeuds):
        nbNoeuds+=2
        
  #tant que la pile n'est pas vide (il reste des sommets/noeuds à parcourir) faire :
  while len(pile)>0:
      sommet_i, C_i = pile.pop() #recuperer sommet_i: le sommet actuel et C_i : la solution actuelle (de l'état courant)
      G[1]=set(list(list_sommets_G))

      #reconstruire le graphe G à l'état actuel (G_i est le graphe G sans la liste des sommets dans l'ensemble des solutions actuelles)
      G_i=supprimerNSommets(G, list(C_i))

      E_i=list(G_i[3].copy()) #recuperer l'ensemble des aretes de G_i

      #si il reste des aretes non couverte dans G_i alors ajouter le sommet actuel à l'ensemble des solutions actuel
      if len(E_i) > 0:
          C_i.add(sommet_i)

      #supprimer le sommet precedement ajouté à la solution
      G_new=supprimerSommet(G_i,sommet_i)

      E_new=list(G_new[3].copy()) #recuperer l'ensemble des aretes de G_new

      if len(E_new) > 0: #si il reste des aretes non couverte dans G_new (G après suppression d'un sommet) alors sauvegarder dans la pile les deux tuples comme au debut
        rd.shuffle(E_new) #randomiser
        arete=E_new[0] #recuperer la premiere arete rencontrée
        sommet1=arete[0] #recuperer le premier sommet de l'arete
        sommet2=arete[1] #recuperer le deuxieme sommet de l'arete

        pile.append((sommet1, C_i.copy()))
        pile.append((sommet2, C_i.copy()))
        
        #incrémenter de 2 le nombre de noeuds générés par le branchement
        if(getNbNoeuds):
            nbNoeuds+=2

      else: #il ne reste plus d'arete à couvrir
        if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_i

        elif(len(C_i) < len(C)): #on a trouver une meilleure solution que celle deja enregistrée donc on la remplace
            C = C_i
      
  
  if(getNbNoeuds):
      return C, nbNoeuds
  else:
      return C


######## 4.2 Ajout des bornes
##Q4.2.2

def calculerBornes (G):
  m=G[2] #recuperer le nombre d'aretes
  n=G[0] #recuperer le nombre de sommets

  #caluler le degrés max de G
  degres=getDegres(G) #retourne un tableau de tuple tel que chaque sommet et associé à son degré
  delta= max([j for (i,j) in degres])

  #Borne sup
  sommets_couplage=list(algo_couplage(G))
  nb_sommets_couplage= len(sommets_couplage)
  Bsup=nb_sommets_couplage  #car l'algorithme du couplage est 2-approché

  #Borne inf
  #caluler b1
  if(delta==0):
    b1=0
  else:
    b1= ceil(m/delta)

  #caluler b2
  b2=nb_sommets_couplage/2 #sachant que algo_couplage retourne une liste de sommets qui verifient une couverture de G, on divise par deux pour avoir le nombre des aretes du couplage

  #caluler b3
  b3= (2*n -1 - sqrt((2*n-1)**2 - 8*m))/2

  Binf=max(b1,b2,b3)

  return Binf, Bsup, sommets_couplage



def branchement_avecBornes(G , getNbNoeuds=False):
                              #getNbNoeuds signifie que l'utilisateur veut connaitre le nombre de noeuds générés par l'algorithme
  nbNoeuds=0
  
  E=list(G[3].copy()) #recuperer l'ensemble des aretes de G
  rd.shuffle(E) #randomiser
  C = set() #initialiser la couverture (la solution a retourner)
  pile=[] #init la pile
  list_sommets_G=frozenset(G[1]) #recuperer l'ensemble des sommets de G

  ## calculer la borne inf et sup de G
  Binf, Bsup, sommets_couplage =calculerBornes(G)
  Bsup_min=Bsup #enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min
  ## Note : Bsup_min sera mise à jour au fur et à mesure où l'on trouve une valeur de Bsup inférieure à celle deja enregistrée

  arete=E[0] #recuperer la premiere arete rencontrée

  sommet1=arete[0] #recuperer le premier sommet de l'arete
  sommet2=arete[1] #recuperer le deuxieme sommet de l'arete

  #incrémenter de 2 le nombre de noeuds générés par le branchement
  if(getNbNoeuds):
        nbNoeuds+=2
   
  #empiler les deux premiers sommets et la solution à l'état initial
  pile.append((sommet1, C.copy()))
  pile.append((sommet2, C.copy()))

  #tant que la pile n'est pas vide (il reste des sommets/noeuds à parcourir) faire :
  while len(pile)>0:
      sommet_i, C_i = pile.pop() #recuperer sommet_i: le sommet actuel et C_i : la solution actuelle (de l'état courant)
      G[1]=set(list(list_sommets_G))

      #reconstruire le graphe G à l'état actuel (G_i est le graphe G sans la liste des sommets dans l'ensemble des solutions actuelles)
      G_i=supprimerNSommets(G, list(C_i))

      E_i=list(G_i[3].copy()) #recuperer l'ensemble des aretes de G_i

      #si il reste des aretes non couverte dans G_i (après avoir supprimé les sommets dans la solution C_i) alors ajouter le sommet actuel à l'ensemble des solutions actuel
      if len(E_i) > 0:
          C_i.add(sommet_i)

      #construire le nouveau graphe G revient à supprimer le sommet precedement ajouté à la solution
      G_new=supprimerSommet(G_i,sommet_i)

      E_new=list(G_new[3].copy()) #recuperer l'ensemble des aretes de G_new

      #verifier si C_i est une solution
      if len(E_new) > 0: #si il reste des aretes non couverte dans G' (G après suppression d'un sommet) alors sauvegarder dans la pile les deux tuples comme au debut

        Binf, Bsup, sommets_couplage= calculerBornes(G_new)
        Bsup=Bsup+len(C_i) ## Bsup est égale à la taille du couplage plus le nombre de sommets dans la solution actuelle

        if(Bsup_min>Bsup):
          Bsup_min=Bsup  ## enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min

        ## traiter les cas où il faut élaguer les noeuds
        if(Binf==Bsup): ## élaguer le noeud car on est sur d'avoir une solution égale à |C_i|+Bsup (ou Binf qui est égale à sommets_couplage) dans les sommets enfanst donc inutile de les parcourir
          C_e= set(list(C_i)+sommets_couplage)

          if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_e

          elif(len(C_e) < len(C)): #si la solution au niveau du noeud qu'on veut élaguer est une meilleure solution que celle deja enregistrée alors on la remplace
            C = C_e

        elif (Binf>Bsup_min): ## élaguer le noeud car on est sur que la solution obtenu est moins bonne qu'une autre solution deja découverte
          pass #soit pas empiler les sommets enfants

        else :
          rd.shuffle(E_new) #randomiser
          arete=E_new[0] #recuperer la premiere arete rencontrée
          sommet1=arete[0] #recuperer le premier sommet de l'arete
          sommet2=arete[1] #recuperer le deuxieme sommet de l'arete
            
          pile.append((sommet1, C_i.copy()))
          pile.append((sommet2, C_i.copy()))
            
          #incrémenter de 2 le nombre de noeuds générés par le branchement
          if(getNbNoeuds):
                nbNoeuds+=2

      else: #il ne reste plus d'arete à couvrir donc C_i est une solution
        if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_i

        elif(len(C_i) < len(C)): #si on a trouver une meilleure solution que celle deja enregistrée donc on la remplace
            C = C_i
      
  
  if(getNbNoeuds):
      return C, nbNoeuds
  else:
      return C


######## 4.3 Amelioration du branchement
##Q4.3.1

def branchement_ameliore(G, getNbNoeuds=False):
                            #getNbNoeuds signifie que l'utilisateur veut connaitre le nombre de noeuds générés par l'algorithme
  nbNoeuds=0
  
  E=list(G[3].copy()) #recuperer l'ensemble des aretes de G
  rd.shuffle(E) #randomiser
  C = set() #initialiser la couverture (la solution a retourner)
  pile=[] #init la pile
  list_sommets_G=frozenset(G[1]) #recuperer l'ensemble des sommets de G

  ## calculer la borne inf et sup de G
  Binf, Bsup, sommets_couplage =calculerBornes(G)
  Bsup_min=Bsup #enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min
  ## Note : Bsup_min sera mise à jour au fur et à mesure où l'on trouve une valeur de Bsup inférieure à celle deja enregistrée

  arete=E[0] #recuperer la premiere arete rencontrée

  sommet=arete[0] #recuperer le premier sommet de l'arete

  """empiler le premier sommet, avec un marqueur "True" si sommet1 est pris, et "False" si sommet n'est pas pris mais que tous ses voisins le sont
  la solution à l'état initial (C vide) """;
  pile.append((sommet,False, C.copy()))
  pile.append((sommet,True, C.copy()))
  
  #incrémenter de 2 le nombre de noeuds générés par le branchement
  if(getNbNoeuds):
        nbNoeuds+=2
   
  #tant que la pile n'est pas vide (il reste des sommets/noeuds à parcourir) faire :
  while len(pile)>0:
      sommet_i, etat_i , C_i = pile.pop() #recuperer sommet_i: le sommet actuel et C_i : la solution actuelle (de l'état courant)
      G[1]=set(list(list_sommets_G))

      #reconstruire le graphe G à l'état actuel (G_i est le graphe G sans la liste des sommets dans l'ensemble des solutions actuelles)
      G_i=supprimerNSommets(G, list(C_i))

      E_i=list(G_i[3].copy()) #recuperer l'ensemble des aretes de G_i

      #si il reste des aretes non couverte dans G_i (après avoir supprimé les sommets dans la solution C_i) alors ajouter le sommet actuel à l'ensemble des solutions actuel
      if len(E_i) > 0:

        #-- si etat==False alors ajouter les voisins de sommet à l'ensemble des solutions actuelles sinon ajouter le sommet
        if(etat_i==False):

          #recuperer les voisins de sommet_i
          voisins_i=getVoisins(G_i,sommet_i)

          C_i=C_i.union(voisins_i) #mettre a jours la solution

          #construire le nouveau graphe G revient à supprimer le sommet precedement ajouté à la solution
          G_new=supprimerNSommets(G_i,voisins_i)

        else :
          C_i.add(sommet_i) #mettre a jours la solution

          #construire le nouveau graphe G revient à supprimer le sommet precedement ajouté à la solution
          G_new=supprimerSommet(G_i,sommet_i)

      E_new=list(G_new[3].copy()) #recuperer l'ensemble des aretes de G_new

      #verifier si C_i est une solution
      if len(E_new) > 0: #si il reste des aretes non couverte dans G' (G après suppression d'un sommet) alors sauvegarder dans la pile les deux tuples comme au debut

        Binf, Bsup, sommets_couplage= calculerBornes(G_new)
        Bsup=Bsup+len(C_i) ## Bsup est égale à la taille du couplage plus le nombre de sommets dans la solution actuelle

        if(Bsup_min>Bsup):
          Bsup_min=Bsup  ## enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min

        ## traiter les cas où il faut élaguer les noeuds
        if(Binf==Bsup): ## élaguer le noeud car on est sur d'avoir une solution égale à |C_i|+Bsup (ou Binf qui est égale à sommets_couplage) dans les sommets enfanst donc inutile de les parcourir
          C_e= set(list(C_i)+sommets_couplage)

          if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_e

          elif(len(C_e) < len(C)): #si la solution au niveau du noeud qu'on veut élaguer est une meilleure solution que celle deja enregistrée alors on la remplace
            C = C_e

        elif (Binf>Bsup_min): ## élaguer le noeud car on est sur que la solution obtenu est moins bonne qu'une autre solution deja découverte
          pass #soit pas empiler les sommets enfants

        else :
          rd.shuffle(E_new) #randomiser
          arete=E_new[0] #recuperer la premiere arete rencontrée
          sommet=arete[0] #recuperer un sommet de l'arete

          pile.append((sommet,False, C_i.copy()))
          pile.append((sommet,True, C_i.copy()))
        
          #incrémenter de 2 le nombre de noeuds générés par le branchement
          if(getNbNoeuds):
                nbNoeuds+=2

      else: #il ne reste plus d'arete à couvrir donc C_i est une solution

        if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_i

        elif(len(C_i) < len(C)): #si on a trouver une meilleure solution que celle deja enregistrée donc on la remplace
            C = C_i
      
  if(getNbNoeuds):
      return C, nbNoeuds
  else:
      return C



##Q4.3.1

def branchement_ameliore_maxDeg(G, getNbNoeuds=False):
                            #getNbNoeuds signifie que l'utilisateur veut connaitre le nombre de noeuds générés par l'algorithme
  nbNoeuds=0
  
  E=list(G[3].copy()) #recuperer l'ensemble des aretes de G
  rd.shuffle(E) #randomiser
  C = set() #initialiser la couverture (la solution a retourner)
  pile=[] #init la pile
  list_sommets_G=frozenset(G[1]) #recuperer l'ensemble des sommets de G

  ## calculer la borne inf et sup de G
  Binf, Bsup, sommets_couplage =calculerBornes(G)
  Bsup_min=Bsup #enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min
  ## Note : Bsup_min sera mise à jour au fur et à mesure où l'on trouve une valeur de Bsup inférieure à celle deja enregistrée

  #- selectionner le sommet de degré max dans G
  sommet=getMaxDegre(G)

  """empiler le premier sommet, avec un marqueur "True" si sommet1 est pris, et "False" si sommet n'est pas pris mais que tous ses voisins le sont
  la solution à l'état initial (C vide) """;
  pile.append((sommet,False, C.copy()))
  pile.append((sommet,True, C.copy()))

  #incrémenter de 2 le nombre de noeuds générés par le branchement
  if(getNbNoeuds):
        nbNoeuds+=2

  #tant que la pile n'est pas vide (il reste des sommets/noeuds à parcourir) faire :
  while len(pile)>0:
      sommet_i, etat_i , C_i = pile.pop() #recuperer sommet_i: le sommet actuel et C_i : la solution actuelle (de l'état courant)
      G[1]=set(list(list_sommets_G))

      #reconstruire le graphe G à l'état actuel (G_i est le graphe G sans la liste des sommets dans l'ensemble des solutions actuelles)
      G_i=supprimerNSommets(G, list(C_i))

      E_i=list(G_i[3].copy()) #recuperer l'ensemble des aretes de G_i

      #si il reste des aretes non couverte dans G_i (après avoir supprimé les sommets dans la solution C_i) alors ajouter le sommet actuel à l'ensemble des solutions actuel
      if len(E_i) > 0:

        #-- si etat==False alors ajouter les voisins de sommet à l'ensemble des solutions actuelles sinon ajouter le sommet
        if(etat_i==False):

          #recuperer les voisins de sommet_i
          voisins_i=getVoisins(G_i,sommet_i)

          C_i=C_i.union(voisins_i) #mettre a jours la solution

          #construire le nouveau graphe G revient à supprimer le sommet precedement ajouté à la solution
          G_new=supprimerNSommets(G_i,voisins_i)

        else :
          C_i.add(sommet_i) #mettre a jours la solution

          #construire le nouveau graphe G revient à supprimer le sommet precedement ajouté à la solution
          G_new=supprimerSommet(G_i,sommet_i)

      E_new=list(G_new[3].copy()) #recuperer l'ensemble des aretes de G_new

      #verifier si C_i est une solution
      if len(E_new) > 0: #si il reste des aretes non couverte dans G' (G après suppression d'un sommet) alors sauvegarder dans la pile les deux tuples comme au debut

        Binf, Bsup, sommets_couplage= calculerBornes(G_new)
        Bsup=Bsup+len(C_i) ## Bsup est égale à la taille du couplage plus le nombre de sommets dans la solution actuelle

        if(Bsup_min>Bsup):
          Bsup_min=Bsup  ## enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min

        ## traiter les cas où il faut élaguer les noeuds
        if(Binf==Bsup): ## élaguer le noeud car on est sur d'avoir une solution égale à |C_i|+Bsup (ou Binf qui est égale à sommets_couplage) dans les sommets enfanst donc inutile de les parcourir
          C_e= set(list(C_i)+sommets_couplage)

          if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_e

          elif(len(C_e) < len(C)): #si la solution au niveau du noeud qu'on veut élaguer est une meilleure solution que celle deja enregistrée alors on la remplace
            C = C_e

        elif (Binf>Bsup_min): ## élaguer le noeud car on est sur que la solution obtenu est moins bonne qu'une autre solution deja découverte
          pass #soit pas empiler les sommets enfants

        else :
          #- selectionner le sommet de degré max dans G_new
          sommet=getMaxDegre(G_new)

          pile.append((sommet,False, C_i.copy()))
          pile.append((sommet,True, C_i.copy()))
          
          #incrémenter de 2 le nombre de noeuds générés par le branchement
          if(getNbNoeuds):
                nbNoeuds+=2

      else: #il ne reste plus d'arete à couvrir donc C_i est une solution

        if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_i

        elif(len(C_i) < len(C)): #si on a trouver une meilleure solution que celle deja enregistrée donc on la remplace
            C = C_i
      
  if(getNbNoeuds):
      return C, nbNoeuds
  else:
      return C


##Q4.4.2

#Cette heuristique fait en sorte de ne tester qu'une seule fois un ensemble de sommets
#par exemple, l'ensemble {0,1,4} sera teste et l'ensemble {1,0,4} ne le sera pas car c'est les memes
def heuristique_branchementAvecBornes(G,getNbNoeuds=False):
                            #getNbNoeuds signifie que l'utilisateur veut connaitre le nombre de noeuds générés par l'algorithme
  nbNoeuds=0
  
  E=list(G[3].copy()) #recuperer l'ensemble des aretes de G
  rd.shuffle(E) #randomiser
  C = set() #initialiser la couverture (la solution a retourner)
  pile=[] #init la pile
  list_sommets_G=frozenset(G[1]) #recuperer l'ensemble des sommets de G

  ## calculer la borne inf et sup de G
  Binf, Bsup, sommets_couplage =calculerBornes(G)

  Bsup_min=Bsup #enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min
  ## Note : Bsup_min sera mise à jour au fur et à mesure où l'on trouve une valeur de Bsup inférieure à celle deja enregistrée

  arete=E[0] #recuperer la premiere arete rencontrée

  sommet1=arete[0] #recuperer le premier sommet de l'arete
  sommet2=arete[1] #recuperer le deuxieme sommet de l'arete

  #empiler les deux premiers sommets et la solution à l'état initial
  pile.append((sommet1, C.copy()))
  pile.append((sommet2, C.copy()))
  
  #incrémenter de 2 le nombre de noeuds générés par le branchement
  if(getNbNoeuds):
        nbNoeuds+=2

  #tant que la pile n'est pas vide (il reste des sommets/noeuds à parcourir) faire :
  while len(pile)>0:
      sommet_i, C_i = pile.pop() #recuperer sommet_i: le sommet actuel et C_i : la solution actuelle (de l'état courant)
      G[1]=set(list(list_sommets_G))

      #reconstruire le graphe G à l'état actuel (G_i est le graphe G sans la liste des sommets dans l'ensemble des solutions actuelles)
      G_i=supprimerNSommets(G, list(C_i))

      E_i=list(G_i[3].copy()) #recuperer l'ensemble des aretes de G_i

      #si il reste des aretes non couverte dans G_i (après avoir supprimé les sommets dans la solution C_i) alors ajouter le sommet actuel à l'ensemble des solutions actuel
      if len(E_i) > 0:
          C_i.add(sommet_i)

      #construire le nouveau graphe G revient à supprimer le sommet precedement ajouté à la solution
      G_new=supprimerSommet(G_i,sommet_i)

      E_new=list(G_new[3].copy()) #recuperer l'ensemble des aretes de G_new

      #verifier si C_i est une solution
      if len(E_new) > 0: #si il reste des aretes non couverte dans G' (G après suppression d'un sommet) alors sauvegarder dans la pile les deux tuples comme au debut

        Binf, Bsup, sommets_couplage= calculerBornes(G_new)
        Bsup=Bsup+len(C_i) ## Bsup est égale à la taille du couplage plus le nombre de sommets dans la solution actuelle

        if(Bsup_min>Bsup):
          Bsup_min=Bsup  ## enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min

        ## traiter les cas où il faut élaguer les noeuds
        if(Binf==Bsup): ## élaguer le noeud car on est sur d'avoir une solution égale à |C_i|+Bsup (ou Binf qui est égale à sommets_couplage) dans les sommets enfanst donc inutile de les parcourir
          C_e= set(list(C_i)+sommets_couplage)

          if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_e

          elif(len(C_e) < len(C)): #si la solution au niveau du neoud qu'on veut élaguer est une meilleure solution que celle deja enregistrée alors on la remplace
            C = C_e

        elif (Binf>Bsup_min): ## élaguer le noeud car on est sur que la solution obtenu est moins bonne qu'une autre solution deja découverte
          pass #soit pas empiler les sommets enfants

        else :
          rd.shuffle(E_new) #randomiser
          arete=E_new[0] #recuperer la premiere arete rencontrée
          sommet1=arete[0] #recuperer le premier sommet de l'arete
          sommet2=arete[1] #recuperer le deuxieme sommet de l'arete

          ### on empile uniquement si le sommet n'est pas deja dans la pile (pour éviter de tester deux fois un meme ensemble de sommets )
          list_sommets_pile=[sommet[0] for sommet in pile] #ce sont les sommets que nous allons parcourir assurement
          if (sommet1 not in list_sommets_pile):
            pile.append((sommet1, C_i.copy()))
            
            #incrémenter de 1 le nombre de noeuds générés 
            if(getNbNoeuds):
                nbNoeuds+=1


          if (sommet2 not in list_sommets_pile):
            pile.append((sommet2, C_i.copy()))
            
            #incrémenter de 1 le nombre de noeuds générés 
            if(getNbNoeuds):
                nbNoeuds+=1

      else: #il ne reste plus d'arete à couvrir donc C_i est une solution
        if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_i

        elif(len(C_i) < len(C)): #si on a trouver une meilleure solution que celle deja enregistrée donc on la remplace
            C = C_i
      
  
  if(getNbNoeuds):
      return C, nbNoeuds
  else:
      return C

#Cette version prend un sommet de degre max a chaque branchement (Nous avons constate une amelioration au niveau de la complexite)
def heuristique_amelioree(G,getNbNoeuds=False):
                            #getNbNoeuds signifie que l'utilisateur veut connaitre le nombre de noeuds générés par l'algorithme
  nbNoeuds=0
  
  E=list(G[3].copy()) #recuperer l'ensemble des aretes de G
  rd.shuffle(E) #randomiser
  C = set() #initialiser la couverture (la solution a retourner)
  pile=[] #init la pile
  list_sommets_G=frozenset(G[1]) #recuperer l'ensemble des sommets de G

  ## calculer la borne inf et sup de G
  Binf, Bsup, sommets_couplage =calculerBornes(G)

  Bsup_min=Bsup #enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min
  ## Note : Bsup_min sera mise à jour au fur et à mesure où l'on trouve une valeur de Bsup inférieure à celle deja enregistrée

  #- selectionner une arete dont l'extremité est de degré max dans G
  sommet_degMax=getMaxDegre(G)
  for e in E:
    if e[0]==sommet_degMax or e[1]==sommet_degMax:
      arete=e
      break
  #- On fait en sorte d'empiler en premier le sommet de degre max pour qu'il soit éliminé lors du parcours des banches du sommet2
  sommet1=sommet_degMax #recuperer le premier sommet de l'arete
  if(arete[1]==sommet_degMax):
    sommet2=arete[0]
  else:
    sommet2=arete[1]

  #empiler les deux premiers sommets et la solution à l'état initial
  pile.append((sommet1, C.copy()))
  pile.append((sommet2, C.copy()))

  #incrémenter de 2 le nombre de noeuds générés 
  if(getNbNoeuds):
    nbNoeuds+=2

  #tant que la pile n'est pas vide (il reste des sommets/noeuds à parcourir) faire :
  while len(pile)>0:
      sommet_i, C_i = pile.pop() #recuperer sommet_i: le sommet actuel et C_i : la solution actuelle (de l'état courant)
      G[1]=set(list(list_sommets_G))

      #reconstruire le graphe G à l'état actuel (G_i est le graphe G sans la liste des sommets dans l'ensemble des solutions actuelles)
      G_i=supprimerNSommets(G, list(C_i))

      E_i=list(G_i[3].copy()) #recuperer l'ensemble des aretes de G_i

      #si il reste des aretes non couverte dans G_i (après avoir supprimé les sommets dans la solution C_i) alors ajouter le sommet actuel à l'ensemble des solutions actuel
      if len(E_i) > 0:
          C_i.add(sommet_i)

      #construire le nouveau graphe G revient à supprimer le sommet precedement ajouté à la solution
      G_new=supprimerSommet(G_i,sommet_i)

      E_new=list(G_new[3].copy()) #recuperer l'ensemble des aretes de G_new

      #verifier si C_i est une solution
      if len(E_new) > 0: #si il reste des aretes non couverte dans G' (G après suppression d'un sommet) alors sauvegarder dans la pile les deux tuples comme au debut

        Binf, Bsup, sommets_couplage= calculerBornes(G_new)
        Bsup=Bsup+len(C_i) ## Bsup est égale à la taille du couplage plus le nombre de sommets dans la solution actuelle

        if(Bsup_min>Bsup):
          Bsup_min=Bsup  ## enregistrer la valeur de la borne sup minimale afin d'élager un noeud qui présente une Binf tel que Binf>Bsup_min

        ## traiter les cas où il faut élaguer les noeuds
        if(Binf==Bsup): ## élaguer le noeud car on est sur d'avoir une solution égale à |C_i|+Bsup (ou Binf qui est égale à sommets_couplage) dans les sommets enfanst donc inutile de les parcourir
          C_e= set(list(C_i)+sommets_couplage)

          if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_e

          elif(len(C_e) < len(C)): #si la solution au niveau du neoud qu'on veut élaguer est une meilleure solution que celle deja enregistrée alors on la remplace
            C = C_e

        elif (Binf>Bsup_min): ## élaguer le noeud car on est sur que la solution obtenu est moins bonne qu'une autre solution deja découverte
          pass #soit pas empiler les sommets enfants

        else :
          rd.shuffle(E_new) #randomiser

          #- selectionner une arete dont l'extremité est de degré max dans G
          sommet_degMax=getMaxDegre(G_new)
          for e in E_new:
            if e[0]==sommet_degMax or e[1]==sommet_degMax:
              arete=e
              break
          #- On fait en sorte d'empiler en premier le sommet de degre max pour qu'il soit éliminé lors du parcours des banches du sommet2
          sommet1=sommet_degMax #recuperer le premier sommet de l'arete
          if(arete[1]==sommet_degMax):
            sommet2=arete[0]
          else:
            sommet2=arete[1]

          ### on empile uniquement si le sommet n'est pas deja dans la pile (pour éviter de tester deux fois un meme ensemble de sommets )
          list_sommets_pile=[sommet[0] for sommet in pile] #ce sont les sommets que nous allons parcourir assurement
          if (sommet1 not in list_sommets_pile):
            pile.append((sommet1, C_i.copy()))
            
            #incrémenter de 1 le nombre de noeuds générés 
            if(getNbNoeuds):
                nbNoeuds+=1


          if (sommet2 not in list_sommets_pile):
            pile.append((sommet2, C_i.copy()))
            
            #incrémenter de 1 le nombre de noeuds générés 
            if(getNbNoeuds):
                nbNoeuds+=1

      else: #il ne reste plus d'arete à couvrir donc C_i est une solution
        if (len(C) == 0): #premiere fois qu'on trouve une solution (premier parcours)
            C = C_i

        elif(len(C_i) < len(C)): #si on a trouver une meilleure solution que celle deja enregistrée donc on la remplace
            C = C_i
      
  if(getNbNoeuds):
      return C, nbNoeuds
  else:
      return C

