# -*- coding: utf-8 -*-
"""RI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o764jw7cvL_8xtEABjR6Zu1vr0yFNIxK

Dans ce mini projet, il est demandé de concevoir un système de recherche d'information en implémentant deux modèles de base:


*   Modèle vectoriel
*   Modèle booléen


Puis, effectuer les expérimentations nécessaires afin de fixer le seuil et la taille de réponse


Vous pouvez trouver a la fin une section pour tester les modèles. Cependant nous avons établie une interface pour le teste en générale


---

Redirectionner vers le dossier du projet RI dans le drive
"""

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/RI

# Commented out IPython magic to ensure Python compatibility.
# %ls

"""Les imports nécessaires pour le bon fonctionnement de notre mini-projet"""

import re
import pickle
import time
import collections
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math
import os
from collections import OrderedDict

import nltk
nltk.download('punkt')
nltk.download('stopwords')

"""#Extraction des documents

Lecture de la collection

---
"""

#Ouverture de cacm.all
c=open("cacm.all","r")
var=c.readlines()

"""Extraction des documents des collections

---


"""

start_time = time.time()  

Liste_Textes=[] 
#Extraire les blocs de documents à partir de .I ..... jusqu'à ...... .X
for i in var:
	if i.startswith('.I'):
		Texte=''
	Texte=Texte+str(i)
	if i.startswith('.X'):
		Liste_Textes.append(Texte)

Documents={}
for texte_doc in Liste_Textes:
	y=re.search(".I\s(\d*)\n.T((.|\n)*?)(.W\n((.*\n)*))?(.B(.|\n)*?)(.A\n((.*\n)*))?.N",str(texte_doc))
	if y:
		Documents[str(y.group(1))]=str(y.group(2))
		if(y.group(5)):
			Documents[str(y.group(1))]=Documents[str(y.group(1))]+str(y.group(5))
		if(y.group(10)):
			Documents[str(y.group(1))]=Documents[str(y.group(1))]+str(y.group(10))

interval = time.time() - start_time  
print ("Temps d'extraction  %.02f" % (interval)," secondes"  )

"""Sauvegarder les documents dans un fichier pickle

---


"""

#Stocker les documents dans un fichier pickle
outfile = open("./pickle/Documents",'wb')
pickle.dump(Documents,outfile)

file_stats = os.stat("./pickle/Documents")
print(f'Taille documents en MegaBytes est {file_stats.st_size / (1024 * 1024)}')

"""#Indexation

Récupérer les documents de la collection

---
"""

#ouverture du fichier contenant les documents
infile = open("./pickle/Documents",'rb')
Documents= pickle.load(infile)      #Documents est un dictio clé: num du document ------> Valeur: titre+ résumé+ Auteur

"""Visualiser les documents de la collections

---


"""

Documents

"""##fichier indexe

La fonction traiter_document est une fonction qui permet d'effectuer un prétraitement sur les documents


---
"""

def traiter_document(var):
	#remplacer les '
	var=var.replace(","," ")
	var=var.replace("."," ")
	var=var.replace("-"," ")
	var=var.replace("!"," ")
	var=var.replace("?"," ")
	var=var.replace(":"," ")
	var=var.replace("="," ")
	var=var.replace("@"," ")
	var=var.replace("&"," ")
	var=var.replace("$"," ")
	var=var.replace("("," ")
	var=var.replace(")"," ")
	var=var.replace("["," ")
	var=var.replace("]"," ")
	var=var.replace("{"," ")
	var=var.replace("}"," ")
	var=var.replace("<"," ")
	var=var.replace(">"," ")
	var=var.replace("'"," ")
	var=var.replace("`"," ")
	var=var.replace("|"," ")
	ponctuation=["\"", "'", "!", "(", ")", "?", ":", "=", ",", ";", ".","`",">","<","}","{","]","[","&","@","|"]

	#decouper le texte en mots et mettre tous les mots en minuscules
	liste_des_mots=word_tokenize(var)
	#liste_des_mots = [word.lower() for word in liste_des_mots ]
	
	#supprimer les mots vides
	#print(stopwords.words('english'))
  
	liste_des_mots = [word for word in liste_des_mots if word.lower() not in stopwords.words("english")]
  

	#supprimer la ponctuation
	liste_des_mots = [word for word in liste_des_mots if word not in ponctuation]

	#supprimer les mots à une seule lettre
	liste_des_mots = [word for word in liste_des_mots if len(word)>1]

	#calcuer la frequence de chaque mot du document et mettre le tout dans un dictionnaire "dict_frequence"
	dict_frequence=dict(collections.Counter(liste_des_mots))

	return(dict_frequence)

"""Création du fichier index en calculant le temps d'exécution

---


"""

#dict contenant l'index
index=dict()

start_time = time.time()  
#indexer tous les documents
for cle in Documents.keys():
	var=Documents[cle]
	index[cle]=traiter_document(var)
 
interval = time.time() - start_time  
print ("Temps dde création du fichier indexe  %.02f" % (interval)," secondes"  )

"""Sauvegarder l'index dans un fichier pickle

---


"""

#Stocker le fichier index dans un fichier pickle
outfile1 = open("./pickle/index",'wb')
pickle.dump(index,outfile1)

"""Mesurer la taille physique du fichier index

---


"""

file_stats = os.stat("./pickle/index")
print(f'Taille index en MegaBytes est {file_stats.st_size / (1024 * 1024)}')

"""## fichier inverse

Création du fichier inverse

---
"""

#Fonction de creation du fichier inverse  (mot,doc) -------> frequence 
def reverse_document(index):
	reverse_dic = dict()
	for numdoc,value in index.items():
		num = numdoc
		for worddic,frequencydic in value.items():
			word = worddic
			frequency = frequencydic
			#print(num,word,frequency)
			reverse_dic[(word,num)] =frequency
	return reverse_dic

#dict contenant le fichier inverse (mot,doc) -------> frequence
reverse_dic =dict()

start_time = time.time() 
reverse_dic = reverse_document(index)
interval = time.time() - start_time  
print ("Temps dde création du fichier inverse avec fréquence  %.02f" % (interval)," secondes"  )

#Stocker le fichier inverse dans un fichier pickle
outfile3 = open("./pickle/Fichier_inverse_meth1",'wb')
pickle.dump(reverse_dic,outfile3)

file_stats = os.stat("./pickle/Fichier_inverse_meth1")
print(f'Taille inverse en MegaBytes est {file_stats.st_size / (1024 * 1024)}')

"""##fichier inverse podéré"""

def poids(ti,dj):
    freqtidj = reverse_dic[(ti,dj)]  # ----> freq(ti,dj) 
    freqdj = sorted(list(index[dj].values()), reverse=True)[0]   # ---> max(freq(dj))
    N = 3204
    #ni
    mylist = [mot for mot in list(reverse_dic.keys()) if mot[0]==ti]
    ni = len(mylist)
    return float("{:.3f}".format((freqtidj/freqdj)*math.log10((N/ni)+1)))

#Fonction de creation du fichier inverse pondere (mot,doc) ----> ponderation
def reverse_document_pondere(reverse_dic):
	reverse_dic_pondere = dict()
	for key in reverse_dic.keys():
		reverse_dic_pondere[key] = poids(key[0], key[1])
	return reverse_dic_pondere

#dict contenant le fichier inverse (mot,doc) -------> pondération
reverse_dic_pondere =dict()

start_time = time.time() 
#Construction d'un fichier inverse pondéré
reverse_dic_pondere = reverse_document_pondere(reverse_dic)
interval = time.time() - start_time  
print ("Temps de création du fichier inverse pondéré  %.02f" % (interval)," secondes"  )

#Stocker le fichier inverse pondéré dans un fichier pickle
outfile4 = open("./pickle/Fichier_inverse_pondere",'wb')
pickle.dump(reverse_dic_pondere, outfile4)

file_stats = os.stat("./pickle/Fichier_inverse_pondere")
print(f'Taille inverse pondéré en MegaBytes est {file_stats.st_size / (1024 * 1024)}')

"""#les fonctions d'acces"""

def Accès_par_dic(num_Doc):
	return index[num_Doc]

def Accès_par_mot(mot):
	return Fichier_inverse[mot]

def Accès_par_mot_doc(mot,num_Doc):
	return Fichier_inverse_meth1[(mot,num_Doc)]

"""#les modèles

##Modéle booléen
"""

def Modèle_Boolean(Request,Index):
    #liste qui contiendera les documents vérifiés
    Reponse_Documents=[]
    #tokenization de la requête
    Requete_tokens=nltk.tokenize.word_tokenize(Request)  
    #Requete_tokens=['(','eau','and','poisson',')','or','chèvre']
    # stocker dans une liste les termes de la requete sans les operateur 
    Liste_termes_Req=[]
    for exp in Requete_tokens:
            if(exp.lower() not in ['and','or','(',')','not']):
                Liste_termes_Req.append(exp)
   
    #Parcourir tous les documents de l'index
    for doc in Index.keys():
        #print('doc'+str(doc))
        #pour chaque document on a besoin d'une nouvelle copie des tokens de a requete
        #Requete=Requete_tokens 
        Requete=nltk.tokenize.word_tokenize(Request)  
        #Requete=['(','eau','and','poisson',')','and','not','chèvre']
        #print(Liste_termes_Req)
        for terme in Liste_termes_Req:
            #print(terme)
            if(terme in Index[doc].keys()):
                #print(Requete)
                Requete[Requete.index(terme)]='1'
                #print('oui')
            else:
                Requete[Requete.index(terme)]='0'
                #print('non')
        
        String_Requete=" ".join(Requete)
        if(eval(String_Requete))==1:
            Reponse_Documents.append(doc)
            #print(Reponse_Documents)
    return(Reponse_Documents)

infile3 = open("./pickle/index",'rb')
index= pickle.load(infile3) 

infile = open("./pickle/Fichier_inverse_meth1",'rb')
reverse_dic= pickle.load(infile) 

infile = open("./pickle/Fichier_inverse_pondere",'rb')
reverse_dic_pondere= pickle.load(infile)

"""Tester quelque requetes avec le modèle booléen

---


"""

Requ='(preliminary or (report and time)) and not computer'

start_time = time.time()
reponse = Modèle_Boolean(Requ,index)
print(reponse)
interval = time.time() - start_time  
print ("Temps de réponse du modele booleen  %.02f" % (interval)," secondes"  )

Requ='life and test or ( not open and books )'

start_time = time.time()
reponse = Modèle_Boolean(Requ,index)
print(reponse)
interval = time.time() - start_time  
print ("Temps de réponse du modele booleen  %.02f" % (interval)," secondes"  )

Requ="(science or compiler) and not algebra and code"

start_time = time.time()
reponse = Modèle_Boolean(Requ,index)
print(reponse)
interval = time.time() - start_time  
print ("Temps de réponse du modele booleen  %.02f" % (interval)," secondes"  )

Requ="(extraction and roots) or use"

start_time = time.time()
reponse = Modèle_Boolean(Requ,index)
print(reponse)
interval = time.time() - start_time  
print ("Temps de réponse du modele booleen  %.02f" % (interval)," secondes"  )

"""##modele vectoriel

Récupérer les 64 requêtes 

---
"""

c2=open("query.text","r")
var2=c2.readlines()
print(var2)

"""Création d'un dictionnaire contenant les requêtes"""

#créer un dictionnaire de requete
Liste_Textes=[] 
#Extraire les blocs de documents à partir de .I ..... jusqu'à ...... .X
for i in var2:
  if i.startswith('.I'):
    Liste_Textes.append(Texte)
    Texte=''
  Texte=Texte+str(i)
Documents={}
for texte_doc in Liste_Textes:
	y=re.search(".I\s(\d*)\n(.T((.|\n)*?))?(.W\n((.*\n)*))?(.A\n((.*\n)*))?(.N\n((.*\n)*))",str(texte_doc))
	if y:
		Documents[str(y.group(1))]=	''
		if (y.group(6)):
			Documents[str(y.group(1))]=Documents[str(y.group(1))]+str(y.group(6))
		if (y.group(12)):
			Documents[str(y.group(1))]=Documents[str(y.group(1))]+str(y.group(12))
		if (y.group(2)):
			Documents[str(y.group(1))]=Documents[str(y.group(1))]+str(y.group(2))

"""Indexer les requêtes

---


"""

#index requeste
indexReq=dict()
for i in range(1,65):
  indexReq[str(i)] = traiter_document(Documents[str(i)])

"""visualiser l'indexe des requetes

---


"""

print(indexReq)

"""préatratement sur les requetes

---


"""

def cleanReq(var):
    var=var.replace(","," ")
    var=var.replace("."," ")
    var=var.replace("-"," ")
    var=var.replace("!"," ")
    var=var.replace("?"," ")
    var=var.replace(":"," ")
    var=var.replace("="," ")
    var=var.replace("@"," ")
    var=var.replace("&"," ")
    var=var.replace("$"," ")
    var=var.replace("("," ")
    var=var.replace(")"," ")
    var=var.replace("["," ")
    var=var.replace("]"," ")
    var=var.replace("{"," ")
    var=var.replace("}"," ")
    var=var.replace("<"," ")
    var=var.replace(">"," ")
    var=var.replace("'"," ")
    var=var.replace("`"," ")
    var=var.replace("|"," ")
    #var  = var.lower()
    return var

"""Representation des requetes 

---


"""

def codeReq(var,num):
    dicReq = dict()
    index = indexReq[num]
    for term in index:
      freq = index[term]
      maximum = sorted(list(index.values()))[0]
      dicReq[term] = float("{:.3f}".format(freq/maximum))
    return dicReq

"""Les mesures de similarités

---


"""

def mesureInterne(dic_req,reverse_dic_pondere,nbDocument):
    list_doc = dict()
    #construire une liste des documents selectionnée
    dic_doc = dict()
    for iddoc in range(1,(nbDocument+1)):
        somme = 0
        for word in dic_req:
            #calculer la somme des produits interne 
            if (word,str(iddoc)) in reverse_dic_pondere:
                somme = somme + dic_req[word] * reverse_dic_pondere[(word,str(iddoc))]
        #Ajouter le documents a la liste si la somme est différente de zero
        if somme != 0:
            somme = float("{:.3f}".format((somme)))
            dic_doc[str(iddoc)] = somme
    #triée la liste par ordre decroissant
    return dict(sorted(dic_doc.items(), key=lambda item: item[1],reverse=True))

def mesureDice(dic_req,reverse_dic_pondere,nbDocument):
    list_doc = dict()
    #construire une liste des documents selectionnée
    dic_doc = dict()
    for iddoc in range(1,(nbDocument+1)):
        #initialiser les somme
        somme, sommedoc, sommereq = 0,0,0
        for word in dic_req:
            #calculer la somme des produits interne 
            if (word,str(iddoc)) in reverse_dic_pondere:
                somme = somme + dic_req[word] * reverse_dic_pondere[(word,str(iddoc))]
                sommedoc = sommedoc + pow(reverse_dic_pondere[(word,str(iddoc))],2)
                sommereq = sommereq + pow(dic_req[word],2)
        #Ajouter le documents a la liste si la somme est différente de zero
        if somme != 0:
            somme = float("{:.3f}".format(((2*somme) / (sommedoc+sommereq))))
            dic_doc[str(iddoc)] = somme
    #triée la liste par ordre decroissant
    return dict(sorted(dic_doc.items(), key=lambda item: item[1],reverse=True))

def mesureCosinus(dic_req,reverse_dic_pondere,nbDocument):
    list_doc = dict()
    #construire une liste des documents selectionnée
    dic_doc = dict()
    for iddoc in range(1,(nbDocument+1)):
        #initialiser les somme
        somme, sommedoc, sommereq = 0,0,0
        for word in dic_req:
            #calculer la somme des produits interne 
            if (word,str(iddoc)) in reverse_dic_pondere:
                somme = somme + dic_req[word] * reverse_dic_pondere[(word,str(iddoc))]
                sommedoc = sommedoc + pow(reverse_dic_pondere[(word,str(iddoc))],2)
                sommereq = sommereq + pow(dic_req[word],2)
        #Ajouter le documents a la liste si la somme est différente de zero
        if somme != 0:
            somme = float("{:.3f}".format((somme / math.sqrt(sommedoc*sommereq))))
            dic_doc[str(iddoc)] = somme
    #triée la liste par ordre decroissant
    return dict(sorted(dic_doc.items(), key=lambda item: item[1],reverse=True))

def mesureJacard(dic_req,reverse_dic_pondere,nbDocument):
    list_doc = dict()
    #construire une liste des documents selectionnée
    dic_doc = dict()
    for iddoc in range(1,(nbDocument+1)):
        #initialiser les somme
        somme, sommedoc, sommereq = 0,0,0
        for word in dic_req:
            #calculer la somme des produits interne 
            if (word,str(iddoc)) in reverse_dic_pondere:
                somme = somme + dic_req[word] * reverse_dic_pondere[(word,str(iddoc))]
                sommedoc = sommedoc + pow(reverse_dic_pondere[(word,str(iddoc))],2)
                sommereq = sommereq + pow(dic_req[word],2)
        #Ajouter le documents a la liste si la somme est différente de zero
        if somme != 0:
            somme = float("{:.3f}".format((somme / (sommedoc+sommereq-somme))))
            dic_doc[str(iddoc)] = somme
    #triée la liste par ordre decroissant
    return dict(sorted(dic_doc.items(), key=lambda item: item[1],reverse=True))

def Modèle_Vectoriel(req,reverse_dic_pondere,nbDocument):
    print("1- Methode de produit Interne.")
    print("2- Methode de Coefficient de Dice.")
    print("3- Methode de Mesure du Cosinus.")
    print("4- Methode de Mesure du Jaccard.")
    print("Veuillez choisiri votre methode: ")
    methode = int(input())
    if methode == 1:
        print(mesureInterne(req,reverse_dic_pondere,nbDocument))
    elif methode == 2:
        print(mesureDice(req,reverse_dic_pondere,nbDocument))
    elif methode == 3:
        print(mesureCosinus(req,reverse_dic_pondere,nbDocument))
    elif methode == 4:
        print(mesureJacard(req,reverse_dic_pondere,nbDocument))
    else:
        print("Numero incorrecte")

"""Mesurer la similarité avec les requêtes collectés précédemment

---


"""

resultat = dict()
for num in range(1,65):
  dic_req = codeReq(cleanReq(Documents[str(num)]), str(num))
  nbDoc = 3204
  #recuperer les clés du fichier inverse sous forme de liste
  reversed_dic_list = [mot for mot in list(reverse_dic_pondere.keys())]

  print("Requête %d" %num)
  #LE calcul mesure Interne
  start_time = time.time() 
  interne = mesureInterne(dic_req,reverse_dic_pondere,nbDoc)
  interval = time.time() - start_time  
  print ("Temps d'execution de la mesure Interne est  %.02f" % (interval)," secondes"  )
  resultat[(num,'interne')] = (interne, interval)

  #Calcul mesure Dice
  start_time = time.time() 
  dice = mesureDice(dic_req,reverse_dic_pondere,nbDoc)
  interval = time.time() - start_time  
  print ("Temps d'execution de la mesure dice est  %.02f" % (interval)," secondes"  )
  resultat[(num,'dice')] = (dice, interval)

  #Calcul mesure cosinus
  start_time = time.time() 
  cosinus = mesureCosinus(dic_req,reverse_dic_pondere,nbDoc)
  interval = time.time() - start_time  
  print ("Temps d'execution de la mesure cosinus est  %.02f" % (interval)," secondes"  )
  resultat[(num,'cosinus')] = (cosinus, interval)

  #calcul mesure jacard
  start_time = time.time() 
  jacard = mesureJacard(dic_req,reverse_dic_pondere,nbDoc)
  interval = time.time() - start_time  
  print ("Temps d'execution de la mesure jacard est  %.02f" % (interval)," secondes"  )
  resultat[(num,'jacard')] = (jacard, interval)
  print()

"""L'affichage des documents selectionné en utilisant la mesure interne

---


"""

for num in range(1,65):
  print("La liste des documents séléctionné pour la requête %d " %num ," est")
  print("En utilisant la mesure interne: ")
  print(resultat[(num,'interne')][0])
  print()

"""L'affichage des documents selectionné en utilisant la mesure dice

---


"""

for num in range(1,65):
  print("La liste des documents séléctionné pour la requête %d " %num ," est")
  print("En utilisant la mesure dice: ")
  print(resultat[(num,'dice')][0])
  print()

"""L'affichage des documents selectionné en utilisant la mesure cosinus


---


"""

for num in range(1,65):
  print("La liste des documents séléctionné pour la requête %d " %num ," est")
  print("En utilisant la mesure cosinus: ")
  print(resultat[(num,'cosinus')][0])
  print()

"""L'affichage des documents selectionné en utilisant la mesure jaccard


---


"""

for num in range(1,65):
  print("La liste des documents séléctionné pour la requête %d " %num ," est")
  print("En utilisant la mesure jacard: ")
  print(resultat[(num,'jacard')][0])
  print()

"""Sauvegarder les résultats dans un fichier pickle"""

#Stocker le fichier inverse pondéré dans un fichier pickle
outfile4 = open("./pickle/ResultatGlobal",'wb')
pickle.dump(resultat, outfile4)

file_stats = os.stat("./pickle/ResultatGlobal")
print(f'Taille inverse pondéré en MegaBytes est {file_stats.st_size / (1024 * 1024)}')

"""Mesurer le temps d'execution pour la mesure de cosinus

---


"""

starttimeGlobal = time.time()
resultatCosinus = dict()
for num in range(1,65):
  print("Requete %d"%num)
  dic_req = codeReq(cleanReq(Documents[str(num)]), str(num))
  nbDoc = 3204
  #recuperer les clés du fichier inverse sous forme de liste
  reversed_dic_list = [mot for mot in list(reverse_dic_pondere.keys())]


  start_time = time.time() 
  cosinus = mesureCosinus(dic_req,reverse_dic_pondere,nbDoc)
  interval = time.time() - start_time  
  print ("Temps d'execution de la mesure cosinus est  %.02f" % (interval)," secondes"  )
  resultatCosinus[num] = (cosinus, interval)
  print()
endtimeGlobal = time.time() - starttimeGlobal
print("Temps de réponse des 64 requêtes est : ", 0.0377)

"""Sauvegarder les résultats de similarités obtenus avec la mesures cosinus

---


"""

#Stocker le fichier inverse pondéré dans un fichier pickle
outfile4 = open("./pickle/ResultatCosinus",'wb')
pickle.dump(resultatCosinus, outfile4)

file_stats = os.stat("./pickle/ResultatCosinus")
print(f'Taille inverse pondéré en MegaBytes est {file_stats.st_size / (1024 * 1024)}')

"""#Evaluation des requetes

récupération des requêtes pertinente

---
"""

req_file = open("qrels.text",'r')
var=req_file.readlines() 
liste_des_mots = []
for line in var:
  liste_des_mots.append(word_tokenize(line))
req_dic = dict()
for liste in liste_des_mots:
  
  if(liste[0].startswith('0')):
    if liste[0][1] not in req_dic:
      req_dic[liste[0][1]] = []
    req_dic[liste[0][1]].append(liste[1])
  else:
    if liste[0] not in req_dic:
      req_dic[liste[0]] = []
    req_dic[liste[0]].append(liste[1])

cosinus = open("./pickle/ResultatCosinus",'rb')
Cos = pickle.load(cosinus)

"""##Rappel"""

def Recall(requette, doc_list):
  #Le nombre de documents partinant en total
  nbDocPartinantTotal = len(requette)
  #Le nombre de documents partiant selectionne
  nbDocPartinantSelectionne = 0
  for doc in doc_list:
    if doc in requette:
      nbDocPartinantSelectionne = nbDocPartinantSelectionne + 1
  recall = nbDocPartinantSelectionne / nbDocPartinantTotal
  return recall

starttimerecall = time.time()
recall_result = dict()
for key in req_dic.keys():
  doc_list = []
  for tupe in Cos[(int(key))][0]:
    doc_list.append(tupe)
  #La requette
  requette = req_dic[key]
  #Calculer le rappel pour chaque requête
  recall_result[key] = Recall(requette, doc_list)  
  print("Le rappel de la requêtte %s "%key, "est %f"% recall_result[key])
endtimerecall = time.time() - starttimerecall
print("Le temps de mesure de rappel est ",endtimerecall )

outfile4 = open("./pickle/recallResult",'wb')
pickle.dump(recall_result, outfile4)

"""##Precision"""

def Precision(requette, doc_list):
  #Le nombre de documents partinant en total
  nbDocPartinantTotal = len(doc_list)
  #Le nombre de documents partiant selectionne
  nbDocPartinantSelectionne = 0
  for doc in doc_list:
    if doc in requette:
      nbDocPartinantSelectionne = nbDocPartinantSelectionne + 1
  precision = nbDocPartinantSelectionne / nbDocPartinantTotal
  return precision

starttimeprecision = time.time()
precision_result = dict()
for key in req_dic.keys():
  doc_list = []
  for tupe in Cos[(int(key))][0]:
    doc_list.append(tupe)
  #La requette
  requette = req_dic[key]
  #Calculer le rappel pour chaque requête
  precision_result[key] = Precision(requette, doc_list)
  print("La precision de la requêtte %s"%key, " est %f"%precision_result[key]) 
endtimeprecision = time.time() - starttimeprecision
print("Le temps de calcul de la precision est ", endtimeprecision)

outfile4 = open("./pickle/precisionResult",'wb')
pickle.dump(precision_result, outfile4)

"""#Experimentals"""

def mesureCosinusSeuil(dic_req,reverse_dic_pondere,nbDocument, seuilMin):
    list_doc = dict()
    #construire une liste des documents selectionnée
    dic_doc = dict()
    for iddoc in range(1,(nbDocument+1)):
        #initialiser les somme
        somme, sommedoc, sommereq = 0,0,0
        for word in dic_req:
            #calculer la somme des produits interne 
            if (word,str(iddoc)) in reverse_dic_pondere:
                somme = somme + dic_req[word] * reverse_dic_pondere[(word,str(iddoc))]
                sommedoc = sommedoc + pow(reverse_dic_pondere[(word,str(iddoc))],2)
                sommereq = sommereq + pow(dic_req[word],2)
        #Ajouter le documents a la liste si la somme est différente de zero
        if somme != 0 :
            somme = float("{:.3f}".format((somme / math.sqrt(sommedoc*sommereq))))
            if( somme > seuilMin):
              dic_doc[str(iddoc)] = somme
    #triée la liste par ordre decroissant
    return dict(sorted(dic_doc.items(), key=lambda item: item[1],reverse=True))

"""## Experimentation Seuil

###Mesure

Dans cette partie, nous varions le seuilMin manuellement de 0.1 à 0.9

---
"""

seuilMin = 0.9

for num in range(1,65):
  dic_req = codeReq(cleanReq(Documents[str(num)]), str(num))
  nbDoc = 3204
  start_time = time.time() 
  cosinus = sorted(mesureCosinusSeuil(dic_req,reverse_dic_pondere,nbDoc,seuilMin).items(), key=lambda t: t[1], reverse=True)
  interval = time.time() - start_time  
  resultat[num] = (cosinus,seuilMin,interval)
recall_result = dict()
for key in req_dic.keys():
  doc_list = []
  for tupe in resultat[(int(key))][0]:
    doc_list.append(tupe[0])
  #La requette
  requette = req_dic[key]
  #Calculer le rappel pour chaque requête
  recall_result[key] = Recall(requette, doc_list)  
outfile4 = open("./pickle/recallSeuil"+str(seuilMin),'wb')
pickle.dump(recall_result, outfile4)

precision_result = dict()
for key in req_dic.keys():
  doc_list = []
  for tupe in resultat[(int(key))][0]:
    doc_list.append(tupe[0])
  #La requette
  requette = req_dic[key]
  #Calculer le rappel pour chaque requête
  precision_result[key] = Precision(requette, doc_list) 
#sauvegarder dans un fichier pickle
outfile4 = open("./pickle/precisionSeuil"+str(seuilMin),'wb')
pickle.dump(precision_result, outfile4)

"""###Compare

Comparer les seuil et sauvegarder les résultats (prcision rappel)

---
"""

seuilGlobal = dict()
seuilMinlist = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
for key in req_dic.keys():
  for seuilMin in seuilMinlist:
    outfile4 = open("recallSeuil"+str(seuilMin),'rb')
    recall1 = pickle.load(outfile4)
    outfile4 = open("precisionSeuil"+str(seuilMin),'rb')
    precision1 = pickle.load(outfile4)
    #(key,seuil) => (recall, precision)
    print("("+ str(key)+ ","+str(seuilMin)+ ") => "+ "(" + str(recall1[str(key)])+"," + str(precision1[str(key)])+ ")")
    seuilGlobal[(key,seuilMin)] = (recall1[str(key)],precision1[str(key)])

outfile4 = open("./pickle/SeuilRequetteGlobal",'wb')
pickle.dump(seuilGlobal, outfile4)

outfile4 = open("./pickle/SeuilRequetteGlobal",'rb')
seuilGlobal = pickle.load(outfile4)
seuilGlobal

"""###Meuilleur configuration pour le seuil"""

outfile4 = open("./pickle/SeuilRequetteGlobal",'rb')
bestseuilFile = pickle.load(outfile4)
print(bestseuilFile)

liste = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
bestconfig = dict()
for key in req_dic.keys():
  max = bestseuilFile[(str(key),0.1)][0]
  maxseuil = 0.1
  for seuil in liste:
    if bestseuilFile[(str(key),seuil)][0] > max:
      max = bestseuilFile[(str(key),seuil)][0]
      maxseuil = seuil
  bestconfig[int(key)] = maxseuil

print(dict(sorted(bestconfig.items(), key=lambda item: item[0],reverse=True)))

outfile4 = open("./pickle/SeuilApresExperimentation",'wb')
pickle.dump(bestconfig, outfile4)

"""##Experiemntation taille"""

outfile4 = open("./pickle/ResultatCosinus",'rb')
cosinuslist = pickle.load(outfile4)

#calcul des precisions en variant les tailles
recall_result = dict()
precision_result = dict()
resultat_taille = dict()
for key in req_dic.keys():
  dic_req = codeReq(cleanReq(Documents[str(key)]), str(key))
  seuile = bestconfig[int(key)]
  #seuile = 0.2
  nbDoc = 3204
  requette = req_dic[key]
  for taille in range(1,len(cosinuslist[int(key)][0]),1):
    cosinus = sorted(mesureCosinusSeuil(dic_req,reverse_dic_pondere,nbDoc,seuile).items(), key=lambda t: t[1], reverse=True)[:taille]
    #resultat_taille[(key,taille)] = cosinus
    doc_list = []
    for tupe in cosinus:
      doc_list.append(tupe[0])
    
    resultat_taille[(key,taille)] = (Recall(requette, doc_list),Precision(requette, doc_list) )

print(resultat_taille)

outfile4 = open("./pickle/TailleExperimentation",'wb')
pickle.dump(resultat_taille,outfile4)

"""###Meuilleur configuration de taille

Meuilleur cofiguration pour la taille pour chaque requette
"""

outfile4 = open("./pickle/TailleExperimentation",'rb')
tailleFile = pickle.load(outfile4)

bestconfig = dict()
for key in req_dic.keys():
  max = tailleFile[(str(key),1)]
  maxtaille = 1
  for taille in range(1,len(cosinuslist[int(key)][0]),1):
    if tailleFile[(str(key),taille)] > max:
      max = tailleFile[(str(key),taille)]
      maxtaille = taille
  bestconfig[int(key)] = maxtaille

print(bestconfig)

outfile4 = open("./pickle/TailleApresExperimentation",'wb')
pickle.dump(bestconfig, outfile4)

"""**Merci pour votre lecture**"""