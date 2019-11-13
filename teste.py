from flask import Flask, render_template, request
from static.plt.graph import build_graph
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np
import csv
import json

app = Flask(__name__)

@app.route('/IPCA')
def IPCA():
    return render_template('IPCA.html')



@app.route('/respostaIPCA', methods=['POST'])
def respostaIPCA():
    lista_de_mes = []
    lista_de_datas = []

    with open('static/Séries de estatísticas.csv', encoding='iso-8859-1') as query:
        data = csv.reader(query, delimiter='\t')  

        mes = int(request.form['meses'])

        for linha in data:
            nova_linha = linha[0].split(";")
            lista_de_mes.append(nova_linha[mes])
            lista_de_datas.append(nova_linha[0])
        #print(lista_de_medias)

        grafico_1 = build_graph(lista_de_datas,lista_de_mes,'r--','data','variacao','yay')
    return render_template('respostaIPCA.html', grafico=grafico_1)


@app.route('/')
def teste():
    listaDatas = []
    listaValores = []

    with urlopen('https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial=01/01/2019&dataFinal=31/12/2019') as query:
        lista = json.load(query)
        for i in range(len(lista)):
            listaDatas.append(lista[i]["data"])
            listaValores.append(float(lista[i]["valor"]))

    graph = build_graph(listaDatas,listaValores,'b',"datas","indicadores", "indicador silic")

    return render_template("respostaIPCA.html",grafico=graph)
app.run()