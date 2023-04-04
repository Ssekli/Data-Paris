from django.shortcuts import render
from django.http import HttpResponse

import os
import pandas as pd
import csv
import numpy
import numpy as np
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import seaborn as sns
#import io
from io import BytesIO
import base64

from .utils import get_graph, get_GPS
from .ben import nettoyage_df, creation_df_prix, creation_hist_q2

def home(request):
    
    print("HOME")
    print(f"request.POST={request.POST} request.method={request.method}")
    
    if request.method == "POST":
        if request.POST.get("Q1") == "Q1":
            print("++++++++ Q1 clicked")

            graph = Question_1()
            return render(request, 'main/home.html', {"graph":graph})

        elif request.POST.get("Q2") == "Q2":
            print("++++++++ Q2 clicked")

        elif request.POST.get("Q3") == "Q3":
            print("++++++++ Q3 clicked")

            graph = Question_3()
            return render(request, 'main/home.html', {"graph":graph})

        elif request.POST.get("map")[0:3] == "map":
            print("++++++++ MAP clicked")

            arr = "750" + request.POST.get("map")[3:5]
            createMapHtml(arr)
            #graph = Question_3()
            return render(request, 'main/map1.html')

        else:
            print("++++++++ invalid button")

    return render(request, "main/home.html")

def Question_1():

    print(f"++++++++++++++ Q1")
    df_propre = nettoyage_df()
    
    print(f"++++++++++++++ Q1 after nettoyage_df()")
    df_arrondissement = creation_df_prix(df_propre)
    
    print(f"++++++++++++++ Q1 after creation_df_prix()")
    graph = creation_hist_q2(df_arrondissement)

    print(f"++++++++++++++ Q1 after creation_hist_q2()")
    #graph = get_graph()

    return graph

def createMapHtml(arr):

    df = pd.read_csv("/Users/katsuji/Downloads/que-faire-a-paris-.csv", sep=';', header=0)

    print(f"++++++++++++++ arr={arr}")
    get_GPS(arr, df)

    return

def Question_3():

    df = pd.read_csv("/Users/katsuji/Downloads/que-faire-a-paris-.csv", sep=';', header=0)
    
    #get_GPS(33689, df)

    # drop unnecessary columns from DataFrame
    # keep only columns not in list_to_keep
    list_to_keep = ["url", 
                    "lead_text", 
                    "description", 
                    "occurrences", 
                    "date_description", 
                    "cover_url", 
                    "cover_alt", 
                    "cover_credit", 
                    "lat_lon", 
                    "pmr", 
                    "blind", 
                    "deaf", 
                    "transport", 
                    "contact_url", 
                    "contact_phone", 
                    "contact_mail", 
                    "contact_facebook", 
                    "contact_twitter", 
                    "price_detail", 
                    "access_type", 
                    "access_link", 
                    "access_link_text", 
                    "updated_at", 
                    "image_couverture", 
                    "programs", 
                    "address_url", 
                    "address_url_text", 
                    "address_text", 
                    "title_event", 
                    "audience", 
                    "childrens", 
                    "contributor_group"
                    ]
    df_propre = df_cleaning(df)
    df_propr_v2 = df_propre.copy()
    df_tmp = drop_columns(df_propr_v2, list_to_keep)   

    # convert data type (object -> datetime) and define as 
    #       date_start(DateTimeFormat)
    #       date_end(DateTimeFormat)
    # then define another columns : saison

    df_tmp_2 = convert_to_datetime(df_tmp)
    
    # calculate the duration of event and add it to DataFrame.
    #   column added : "duration(days)"
    df_tmp_3 = calculate_duration(df_tmp_2)


    # replace all "NaT" (DateTimeFormat) data with "0"
    # dtype will be changed to "object" and cannot calculate anymore but, anytime it is possible to be change it back to
    # DateTime type by to_datatime() and can calculate
    #
    df_tmp_3.fillna("0", inplace= True)
    # df_tmp.isnull().sum()
    df_propre_v2 = df_tmp_3.copy()

    #df_propre_v2.to_csv('./tmp.csv', header=True, index=False)

    # Free and non-free events by season
    condition_1 = 'price_type'
    price_type_lt = ['gratuit', 'payant']
    condition_3 = 'saison' 
    graph = construct_graph_bar(df_propre_v2, condition_1, price_type_lt, condition_3)

    print("++++++++ Q3 ENDING  ++++++++++++++")
    
    return graph

def df_cleaning(in_df):

    out_df = in_df.copy()

    out_df.dropna(how= 'all', inplace= True)

    out_df.isnull().values.any()
    indexVille = out_df[ out_df["address_city"] != "Paris" ].index
    out_df.drop(indexVille, inplace= True)

    out_df = out_df.reset_index(drop=True)

    return out_df


def drop_columns(in_df, lt):

    in_df.drop(columns=lt, inplace=True)

    return in_df


def convert_to_datetime(df_in):

    sr1 = df_in['date_start']
    sr1 = pd.to_datetime(sr1, errors="coerce")
    sr1 = pd.to_datetime(sr1, utc=True)
    sr1.name="date_start(DateTimeFormat)"

    sr2 = df_in['date_end']
    sr2 = pd.to_datetime(sr2, errors="coerce")
    sr2 = pd.to_datetime(sr2, utc=True)
    sr2.name="date_end(DateTimeFormat)"

    df_out = pd.concat([df_in, sr1, sr2], axis=1)

    # convert to offset aware
    timezone = pytz.timezone("UTC")

    d1 = datetime.strptime('2023-03-21', '%Y-%m-%d')
    d1_aware = timezone.localize(d1)

    d2 = datetime.strptime('2023-06-21', '%Y-%m-%d')
    d2_aware = timezone.localize(d2)

    d3 = datetime.strptime('2023-09-21', '%Y-%m-%d')
    d3_aware = timezone.localize(d3)

    d4 = datetime.strptime('2023-12-21', '%Y-%m-%d')
    d4_aware = timezone.localize(d4)

    mid = sr1 + (sr2 - sr1)

    saison = []

    for i in range(df_out.shape[0]):
        if pd.isnull(mid[i]):
            saison.append("None")
        elif mid[i] >= d1_aware and mid[i] < d2_aware:
            saison.append("printemps")
        elif mid[i] >= d2_aware and mid[i] < d3_aware:
            saison.append("ete")
        elif mid[i] >= d3_aware and mid[i] < d4_aware:
            saison.append("automne")
        else:
            saison.append("hiver")

    tmp_saison = pd.Series(saison)
    tmp_saison.name = "saison"
    df_out = pd.concat([df_out, tmp_saison], axis=1)

    return df_out


def calculate_duration(df_in):

    sr1 = df_in["date_start(DateTimeFormat)"]

    sr2 = df_in["date_end(DateTimeFormat)"]

    sr3 = sr2 - sr1
    sr3.name = "duration(days)"
    df_out = pd.concat([df_in, sr3], axis=1)

    return df_out


def construct_graph_bar(df, condition_1, condition_lt, condition_3):
    # from https://www.youtube.com/watch?v=jrT6NiM46jk&t=185s


    #print(df.columns)
    # remove rows with 'saison' value = "None"
    df = df[df['saison'] != "None"]


    i = 0
    for condition_tmp in condition_lt:
        df_tmp = df[df[condition_1] == condition_tmp]
        df_tmp = df_tmp.groupby(condition_3).count()
        df_tmp = pd.DataFrame(df_tmp['id'])
        df_tmp.reset_index(inplace=True)
        df_tmp['type'] = condition_tmp
        if i == 0:
            df_tmp_2 = df_tmp.copy()
            i += 1
        else:
            df_tmp_2 = pd.concat([df_tmp_2, df_tmp], axis = 0)
    df_tmp_2 = df_tmp_2.reset_index()
    df_tmp_2 = df_tmp_2.drop(columns='index')
    df_tmp_2 = df_tmp_2.reindex(columns=["type", "saison", "id"])
    df_tmp = df_tmp_2.copy()

    new_name = "Nombre d'évènements"
    df_tmp.rename(columns={"id": new_name}, inplace=True)

    sns.set()

    plt.switch_backend('AGG')
    plt.figure(figsize=(9, 5), facecolor="w")
    sns.barplot(data=df_tmp, x="type", y=new_name, hue="saison", hue_order=["printemps", "ete", "automne", "hiver"])
    title = "Nombre d'évènements par payment type"
    plt.title(title)
    
    plt.legend(loc='upper right')

    print("************** ploting ***************")
    #plt.show()

    #buf = io.BytesIO()
    #plt.savefig(buf, format='svg', bbox_inches='tight')
    #s = buf.getvalue()
    #buf.close()

    # output graph plotted by seaborn/matplotlib as image data
    graph = get_graph()

    return graph
    #return render(request, 'main/home.html', {"chart":chart})


