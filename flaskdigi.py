from flask import Flask, abort, jsonify, render_template,url_for, request,send_from_directory,redirect
import numpy as np 
import pandas as pd 
import json
import requests 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

data=pd.read_json('dataDigi.json')
def kombinasi(i):
    return str(i['Stage'])+ '$' +str(i['Type'])+'$'+str(i['attribute'])
data['x']=data.apply(kombinasi,axis=1)
data['Nama']=data['Nama'].apply(lambda i: i.lower())

cov=CountVectorizer(tokenizer=lambda data: data.split('$'))
datamx=cov.fit_transform(data['x'])
skorDigi=cosine_similarity(datamx)


app=Flask(__name__)


@app.route('/')
def home():
    return render_template('digi.html')



@app.route('/CariDigi', methods=['GET','POST'])
def Cari():
    body=request.form
    digimon=body['digimon']
    digimon=digimon.lower()
    if digimon not in list(data['Nama']):
        return redirect('/NotFound')
    indexDigi=data[data['Nama']==digimon].index.values[0]
    favorit=data.iloc[indexDigi][['Nama','Stage','Type','attribute','Pic']]
    DigiScore=list(enumerate(skorDigi[indexDigi]))
    sortDigi=sorted(DigiScore,key=lambda i:i[1],reverse=True)
    rekomen=[]
    for item in sortDigi[:7]:
        x={}
        if data.iloc[item[0]]['Nama'] !=digimon:
            nama=data.iloc[item[0]]['Nama'].capitalize()
            stage=data.iloc[item[0]]['Stage']
            gambar=data.iloc[item[0]]['Pic']
            Type=data.iloc[item[0]]['Type']
            attribute=data.iloc[item[0]]['attribute']
            x['Nama']=nama
            x['stage']=stage
            x['gambar']=gambar
            x['Type']=Type
            x['attribute']=attribute
            rekomen.append(x)
    return render_template('hasil.html',rekomen=rekomen,favorit=favorit)


@app.route('/NotFound')
def notFound():
    return render_template('notfound.html')


if __name__=='__main__':
    app.run(debug=True)