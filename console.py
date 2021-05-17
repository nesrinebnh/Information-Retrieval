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

def Rechrcher_terme(mot):
    infile3 = open("./pickle/Fichier_inverse_meth1",'rb')
    inverse= pickle.load(infile3) 
    start_time = time.time() 
    trouver=False
    for key in inverse.keys():
      if(key[0]) == mot:
        trouver=True
        print("Document "+str(key[1])+"   ------>  Frequence d'apparirion "+str(inverse[key]))
    if trouver == False:
      print("Ce mot n'existe pas dans la collection")

def Accès_par_dic(num_Doc):
  if num_Doc in index: 
	  return index[num_Doc]
  return {}
 
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
    liste_des_mots = [word.lower() for word in liste_des_mots ]
    
    #supprimer les mots vides
    #print(stopwords.words('english'))
    liste_des_mots = [word for word in liste_des_mots if word not in stopwords.words("english")]

    #supprimer la ponctuation
    liste_des_mots = [word for word in liste_des_mots if word not in ponctuation]

    #supprimer les mots à une seule lettre
    liste_des_mots = [word for word in liste_des_mots if len(word)>1]

    #calcuer la frequence de chaque mot du document et mettre le tout dans un dictionnaire "dict_frequence"
    dict_frequence=dict(collections.Counter(liste_des_mots))

    return(dict_frequence)   

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
    var  = var.lower()
    return var

def codeReq(index):
    dicReq = dict()
    for term in index:
      freq = index[term]
      maximum = sorted(list(index.values()), reverse=True)[0]
      dicReq[term] = float("{:.3f}".format(freq/maximum))
    return dicReq

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

def Modèle_Vectoriel(req,reverse_dic_pondere,nbDocument,methode):
    if methode == 1:
        return(mesureInterne(req,reverse_dic_pondere,nbDocument))
    elif methode == 2:
        return(mesureDice(req,reverse_dic_pondere,nbDocument))
    elif methode == 3:
        return(mesureCosinus(req,reverse_dic_pondere,nbDocument))
    elif methode == 4:
        return(mesureJacard(req,reverse_dic_pondere,nbDocument))

#############################################fichier pickle dans le dossier pickle############################        
output = open("./pickle/index",'rb')
index = pickle.load(output)
infile3 = open("./pickle/Fichier_inverse_pondere",'rb')
reverse_dic_pondere= pickle.load(infile3) 


############################################main####################################


menu = int(input("1-Fonction d'acces 2- modele de recherche"))
if menu == 1:
  acces = int(input("Est ce que vous voulez tester les fonctions d'acces? (1 acces par doc et 2 acces par mot "))
  if acces == 2:
    mot = input("Donner un mot: ")
    start_time = time.time()
    Rechrcher_terme(mot)
    interval = time.time() - start_time  
    print ("Temps de réponse  %.02f" % (interval)," secondes"  )
  else:
    num = input("Donner un numero de document: ")
    start_time = time.time()
    dic = Accès_par_dic(num)
    if dic:
      print(dic)
    else:
      print("Le document n'existe pas")
    interval = time.time() - start_time  
    print ("Temps de réponse  %.02f" % (interval)," secondes"  )
else:
  model = int(input("Quelle modele voulez vous tester? (1 pour model booleen et 2 pour model vectoriel"))
  requete = input('Veuillez saisir votre requete: ')
  if(model == 1):
    start_time = time.time()
    reponse = Modèle_Boolean(requete,index)
    print(reponse)
    interval = time.time() - start_time  
    print ("Temps de réponse du modele booleen  %.02f" % (interval)," secondes"  )
  else:
    #tester le modèle vectoriel
    indexreq=traiter_document(requete)
    dicreq=codeReq(indexreq)
    nbDoc = 3204
    start_vect_time = time.time()
    reponse=Modèle_Vectoriel(dicreq,reverse_dic_pondere,nbDoc,2)
    print(reponse)
    intervalvect = time.time() - start_vect_time  
    print ("Temps de réponse du modele vectoriel  %.02f" % (intervalvect)," secondes"  )