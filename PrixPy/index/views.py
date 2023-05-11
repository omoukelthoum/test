from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy



import json
import pandas as pd 
from .models import *


import pymongo 
client = pymongo.MongoClient()
db = client['pie_alpha']
  
# Create your views here.
def Table(request):
    df = pd.read_csv('/Users/User/Desktop/alpha-de-retour/PrixPy/index/static/importation wohooo.csv')
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
  
    return render(request, 'home/archive.html', context)



def pages(request):
    context = {}
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse_lazy('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))


    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


    
def input(request):
    return render(request, '../templates/home/input.html', {})


def index(request):
    context = {'egment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

import pymongo
import pandas as pd
from statistics import mean
from scipy.stats.mstats import gmean
import statistics as s
import numpy as np


   
    

class Uploding():
    def __init__(self, file):
        self.file = file

    def import_base(self):
        df=pd.read_excel(self.file)
        df.columns=['code_fonction','code_groupe','code_sous_groupe','code_poste','code_variete','libelle_court','libelle_long','date_de_creation','date_de_suppression','type',
        'Prix' ,'Importe','Local','Ponderation']
        produit_d=df
     
        produit=json.loads(produit_d.T.to_json()).values()
        db.produit.insert_many(produit)

    def import_monthly(self):
        dt=pd.read_excel(self.file)
        serie=json.loads(dt.T.to_json()).values()
        db.Serie.insert_many(serie)
        print(Serie.objects.all())

def Import_excel(request):
    print("sss")    
    message = 'Importation effectuée avec succés.'
    print(message)
    typeImport=request.POST['typeImport']
    print(typeImport)
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        print('myfile', myfile)
        upload=Uploding(myfile)
        
        if typeImport == 'Base':
                upload.import_base()
                colle= db["produit"]
                data_from_db = colle.find({})
                found=True

        if typeImport == 'Monthly':
                upload.import_monthly()
                colle= db["Serie"]
                data_from_db = colle.find({})
                found=False

    

    
    context = {'datab':data_from_db,'found':found}
    return render(request, '../templates/home/result.html',context)


import pymongo
import pandas as pd
from statistics import mean
from scipy.stats.mstats import gmean
import statistics as s

client = pymongo.MongoClient()
db = client.milouhamboud

def ind_elem_prep(client):
    db = client.milouhamboud
    import bson
    from bson.son import SON
    map = bson.Code(
        """
            function map() {
                emit({  libelle_court : this.Produit, type_p : this.sertyp }, this.prxobs)
            }
            
        """
    )
    reduce = bson.Code(
        """
            function reduce(cle, valeurs) {
                return valeurs;
            }
        """
    )
    results = db.command({'mapReduce': 'Serie','map': map,'reduce': reduce ,"out": SON([('inline',1)])} )
    return results

def final_prix(code_P,nom_P,prix_l,type_p):
    prix_f=[]
    for i in range(len(code_P)):
        if type_p[i]==4:
            prix_f.append(gmean(prix_l[i]))
        else :
            prix_f.append(s.mean(prix_l[i]))
    dataf = {'code_p':code_P , 'libelle_court' : nom_P, 'Prix' : prix_f}
    data=pd.DataFrame(dataf)        
    return  data 
def indice_element(P,nom_P,prix_c,prix_p):
    indice=[]
    for i in range(len(prix_c)):
        indice.append((prix_c[i]/prix_p[i])*100)
    dataf = {'code_p':P , 'libelle_court' : nom_P, 'indice' : indice}
    data=pd.DataFrame(dataf)
    return data
def indice_global(indice_elm,pond,type_imp,type_loc):
    indice_importé= sum([x * y * z for x, y, z in zip(indice_elm,type_imp,pond)])/sum([x * y for x, y in zip(type_imp,pond)])
    indice_Local= sum([x * y * z for x, y, z in zip(indice_elm,type_loc,pond)])/sum([x * y for x, y in zip(type_loc,pond)])
    dic = { 'indice_Local' : [indice_Local] , 'indice_importé' : [indice_importé]}
    df=pd.DataFrame(dic)
    return df

'''
The following is done for data  preparation in order to apply the functions
'''
#----# ind elem prep function #----#
d = ind_elem_prep(client)
df = pd.DataFrame(d)
#-----# cleaning the dict #-----#
df['sep'] = df['results'].apply(lambda cell: cell['_id'])
df['libelle_court'] = df['sep'].apply(lambda cell: cell['libelle_court'])
df['type_p'] = df['sep'].apply(lambda cell: cell['type_p'])
df['Prix'] = df['results'].apply(lambda cell: cell['value'])
df = df.drop(['results','ok','sep'], axis =1)
#----# taking code variete from produit #----#
r = db.produit.find({}, {'libelle_court':1, 'code_variete' :1 , 'Prix' :1})
dataf = pd.DataFrame(r)
dataf = dataf.drop('_id', 1)
dataf.columns = ['code_variete','libelle_court','Prix_base']
df = pd.merge(df,dataf , on =['libelle_court'])
clean =[]
for i in range(len(df.Prix)):
    clean.append([x for x in df.Prix[i] if x != None])
df['Prix'] = clean
for i in range(len(df.Prix)):
            if len(df.Prix[i]) == 0:
                df['Prix'] = df['Prix'].drop(df.index[i])
df = df[df['Prix'].notna()]
df = df.reset_index()    




#----# final prix function #----#
df = final_prix(df['code_variete'],df['libelle_court'],df['Prix'],df['type_p'])
dataf = pd.merge(df,dataf , on =['libelle_court'])

#----# indice element function #----#
dataf = indice_element(dataf.code_p,dataf.libelle_court,dataf.Prix,dataf.Prix_base)

#-----# adding ponderations localy and imported #-----#
y = db.produit.find({}, {'libelle_court':1, 'Importe' :1, 'Local' :1, 'Ponderation' :1})
yy = pd.DataFrame(y)
yy = yy.drop('_id', 1)
dataf = pd.merge(dataf,yy , on =['libelle_court'])
dataf["Importe"] = dataf["Importe"].replace(r'^\s*$', np.nan, regex=True)
dataf["Local"] = dataf["Local"].replace(r'^\s*$', np.nan, regex=True)
dataf["Importe"] = dataf.Importe.astype(float)
dataf["Local"] = dataf.Local.astype(float)
dataf["Importe"] = dataf["Importe"].fillna(0)
dataf["Local"] = dataf["Local"].fillna(0)

#----# indice global function #----#

final = indice_global(dataf.indice, dataf.Ponderation, dataf.Importe,dataf.Local)
final = indice_global(dataf.indice, dataf.Ponderation, dataf.Importe,dataf.Local)
final = final.T
a = dataf.Ponderation[dataf.Local == 1].sum()
b = dataf.Ponderation[dataf.Importe == 1].sum()
final['Ponderation'] = [a,b]
final.columns = ['indice','Ponderation']
# sum(final['Ponderation']) must be 10000 u have 9813 fix it !
new_row = ((final.indice[0]+ final.indice[1]) *final.Ponderation[0] + (final.indice[0]+ final.indice[1]) *final.Ponderation[1] )/(2*10000)
a = {'indice': new_row, 'Ponderation': '-'}
final = final.reset_index()
final = final.append(a,ignore_index=True)
final = final.drop('index',1)
final.index = ['indice_Local','indice_importé','indice_globale']
final = final.drop('Ponderation',1)
final = final.T
final = final.reset_index(drop =True)
    

def ind_elem(request):
    
    if request.method == 'POST' :
        upload=final
        
        

    context = {'loc':upload.indice_Local.values, 'imp':upload.indice_importé.values , 'glob': upload.indice_globale.values}
    return render(request, '../templates/home/import.html',context)



def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

