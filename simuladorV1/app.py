from flask import Flask, render_template, request
from urllib.request import urlopen
import json

app = Flask(__name__)

listaNomeBancos = []
listaTaxaBancos = []

@app.route('/')
def hello():
    i = 0
    with urlopen('https://olinda.bcb.gov.br/olinda/servico/taxaJuros/versao/v2/odata/TaxasJurosDiariaPorInicioPeriodo?$top=50&$format=json&$select=InstituicaoFinanceira,TaxaJurosAoMes,TaxaJurosAoAno,cnpj8') as query:
        lista = json.load(query)
        for item in lista['value']:
            listaNomeBancos.append(lista['value'][i]['InstituicaoFinanceira'])
            listaTaxaBancos.append(lista['value'][i]['TaxaJurosAoMes'])
            i = i + 1
    return render_template('index.html', listaNomeBancos=listaNomeBancos)    


@app.route('/test', methods=['GET','POST'])
def teste():
    if request.method == 'POST':

        nomeBanco = request.form['nome_banco']
        valor = request.form['valor']

        i = 0
        for item in listaNomeBancos:
            if item == nomeBanco:
                return render_template('resultado.html', resultado=str(float(valor) * float(listaTaxaBancos[i]))) 
            else:
                i = i + 1

app.run()