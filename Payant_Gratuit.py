#!/usr/bin/env python
# coding: utf-8

# In[18]:


import os
import pandas
import csv
import numpy
import numpy as np
import pandas as pd
import datetime
import glob
import re
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl


# In[35]:


#Importation du dataframe
df = pandas.read_csv("D:/que-faire-a-paris-.csv", sep= ';', header= 0 )
#on créée une copie
df_propre = df.copy()
df_propre


# In[36]:


#Retire toutes les villes qui ne sont pas "Paris"
indexVille = df_propre[ df_propre["address_city"] != "Paris" ].index
df_propre.drop(indexVille, inplace= True)
#df_propre.reset_index(drop=True)
print(df_propre['address_city'])


# In[22]:


#Afficher les cases nulles
df_propre.isnull()


# In[23]:


#Retire les lignes où il y a des cases nulles 
df_propre.dropna(how='all', inplace=True)
df_propre.isnull().values.any()


print(df_propre['price_type'].value_counts())
print(df_propre.isnull().values.any())


# In[24]:


# selectionne les colonnes au lieu de les supprimer 
df_propre.drop(df_propre.columns.difference(['id', 'title', 'date_start', 'date_end', 'tags', 'address_name', 'address_street', 'address_zipcode', 'lat_lon', 'price_type']
), axis=1, inplace=True)
df_propre


# In[7]:


#Remplacement des événements "gratuit sous condition" par "gratuit"
df_propre_replaced = df_propre.copy()

df_propre_replaced = df_propre_replaced.replace('gratuit sous condition', 'gratuit')

df_propre_replaced


# In[32]:


#Afficher les valeurs du nouveau dataframe après le remplacement des événements "gratuit sous condition" par "gratuit"
print(df_propre_replaced['price_type'].value_counts())


# In[29]:


import matplotlib.pyplot as plt
import seaborn as sns

# Modifier les paramètres par défaut de Matplotlib
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Créer une figure avec une taille de 10 pouces par 10 pouces
plt.figure(figsize=(10, 10))

# Définir les couleurs à utiliser pour chaque part de camembert
colors = sns.color_palette('bright')[0:5]

# Compter le nombre de fois que chaque valeur apparaît
counts = df_propre_replaced['price_type'].value_counts()

# Définir les parts de camembert à séparer
explode = (0.1, 0)

# Créer le graphique de type "camembert éclaté"
plt.pie(counts, colors=colors, explode=explode, labels=counts.index, autopct='%1.1f%%', startangle=90)

# Ajouter un titre au graphique
plt.title("Proportion d'évènements gratuits ou payants", fontsize=20)

# Afficher le graphique
plt.show()

