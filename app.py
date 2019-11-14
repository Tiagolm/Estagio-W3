from flask import Flask, render_template, request
from static.plt.graph import build_graph
from urllib.request import urlopen
from datetime import date, timedelta
import csv
import json

app = Flask(__name__)

listaNomeBancos = []
listaTaxaBancos = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/indicadores')
def indicadores():
    return render_template("indicadores.html")

@app.route('/selic')
def selic():
    listaDatas = []
    listaValores = []

    with urlopen('https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial=01/01/2019&dataFinal=01/10/2019') as query:
        lista = json.load(query)
        for i in range(len(lista)):
            listaDatas.append(lista[i]["data"])
            listaValores.append(float(lista[i]["valor"]))

    graph = build_graph(listaDatas, listaValores, 'b', "datas", "indicadores", "indicador selic")

    return render_template("graficoIndicador.html", grafico=graph)


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

        grafico_1 = build_graph(lista_de_datas, lista_de_mes, 'r--', 'data', f'variacão do mês selecionado', 'IPCA')
    return render_template('graficoIndicador.html', grafico=grafico_1)


@app.route('/tarifas')
def tarifas():
    return render_template("tarifas.html")


@app.route('/respostaTarifas', methods=["POST", "GET"])
def tarifasResposta():
    servico = request.form["servico"]
    with urlopen(
            "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifaPorValores/versao/v1/odata/ListaTarifasPorValores(CodigoGrupoConsolidado=@CodigoGrupoConsolidado,CodigoServico=@CodigoServico)?@CodigoGrupoConsolidado='03'&@CodigoServico='{}'&$top=1000&$format=json".format(
                    servico)) as listaTed:
        dados = json.load(listaTed)

    return render_template("respostaTarifas.html", dados=dados)


@app.route('/simulador')
def simulador():
    i = 0
    with urlopen('https://olinda.bcb.gov.br/olinda/servico/taxaJuros/versao/v2/odata/TaxasJurosDiariaPorInicioPeriodo?$top=50&$format=json&$select=InstituicaoFinanceira,TaxaJurosAoMes,TaxaJurosAoAno,cnpj8') as query:
        lista = json.load(query)
        for item in lista['value']:
            listaNomeBancos.append(lista['value'][i]['InstituicaoFinanceira'])
            listaTaxaBancos.append(lista['value'][i]['TaxaJurosAoMes'])
            i = i + 1
    return render_template('simulador.html', listaNomeBancos=listaNomeBancos)    


@app.route('/respostaSimulador', methods=['GET','POST'])
def respostaSimulador():
    if request.method == 'POST':

        nomeBanco = request.form['nome_banco']
        valor = float(request.form['valor'])
        meses = request.form['meses']


        i = 0
        for item in listaNomeBancos:
            if item == nomeBanco:
                for x in range(int(meses)):
                    valor = round(valor + (valor * listaTaxaBancos[i]), 2)
                return render_template('respostaSimulador.html', resultado=valor) 
            else:
                i = i + 1


@app.route('/conversor')
def conversor():
    return render_template('conversor.html')



@app.route('/conversaoResposta', methods=['POST'])
def dolar():
    data = date.today() - timedelta(days=1)
    data = data.strftime("%m-%d-%Y")

    moeda = request.form['moeda']
    tipo = str(request.form['tipo'])
    
    with urlopen('https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27{}%27&@dataCotacao=%27{}%27&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda'.format(moeda, data)) as query:
        dados = json.load(query)
            
    real_moeda = round((float(request.form['valor']) * float(dados['value'][0][tipo])), 2)

    if(tipo == 'cotacaoCompra'):
        frase = f"Real para Moeda: {moeda}"
    else:
        frase = f"{moeda} para Real"

    return render_template('conversaoResposta.html',valor=real_moeda, tipo=frase)

app.run(debug=True)