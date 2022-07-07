from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pd
import csv
import re
import numpy as np

# Create your views here.


def index(request):
    return render(request,'homepage.html')

def check_tel(tel):
    if len(str(tel)) > 10 or len(str(tel)) < 10 :
        return 1
    else:
        return 0

def validar_correo(correo):
    expresion = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion, correo)is not None


count_nb_rep = 0 
count_cor_rep = 0 
count_tel_rep = 0 

def cargar_datos(request):
    if request.method == "POST":
        file_name = request.FILES['file_name']
        datos = pd.read_csv(file_name)
        datos.columns=['nombre','correo','telefono']

        df = datos.fillna("No tiene")
        df = df.astype(str)
     
        
        def validar_rep(value):
            if df['nombre'].str.contains(value).value_counts()[True] > 1:
                global count_nb_rep 
                count_nb_rep = count_nb_rep + 1
                return True
            else:
                return False

        def validar_rep_correo(value):
            if df['correo'].str.contains(value).value_counts()[True] > 1:
                global count_cor_rep 
                count_cor_rep = count_cor_rep + 1
                return True
            else:
                return False
        def validar_rep_telefono(value):
            if df['telefono'].str.contains(value).value_counts()[True] > 1:
                global count_tel_rep 
                count_tel_rep = count_tel_rep + 1
                return True
            else:
                return False

        df['tel'] = df['telefono'].apply(check_tel)
        df['correo_valido'] = df['correo'].apply(validar_correo)
        df['nombre_rep'] = df['nombre'].apply(validar_rep)
        df['correo_rep'] = df['correo'].apply(validar_rep_correo)
        df['telefono_rep'] = df['telefono'].apply(validar_rep_telefono)
        #se eliminan las filas duplicadas
        df = df.drop_duplicates(['nombre','correo','telefono'], keep='last')
        data =[]
        for i in range(df.shape[0]):
            temp = df.loc[i]
            data.append(dict(temp))

        tot = count_nb_rep + count_cor_rep +count_tel_rep
    
    context = {'data': data,'count':df[df.columns[0]].count(),'registros':datos[datos.columns[0]].count(),'nb_dup': count_nb_rep,'cor_dup':count_cor_rep,'tel_dup': count_tel_rep,'tot_dup': tot }
    return render(request,'homepage.html',context)
