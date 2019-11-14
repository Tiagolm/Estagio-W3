from flask import Flask, render_template, request
from static.plt.graph import build_graph
from urllib.request import urlopen
from datetime import date
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

        grafico_1 = build_graph(lista_de_datas,lista_de_mes,'r--','data',f'variacão do mês selecionado','IPCA')
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
                    valor = valor + (valor * listaTaxaBancos[i])
                return render_template('respostaSimulador.html', resultado=valor) 
            else:
                i = i + 1


@app.route('/conversor')
def conversor():
    return render_template('conversor.html')


#USD
@app.route('/respostaUSD', methods=['GET','POST'])
def conversorUSD():
    if request.method == 'POST':
        return render_template('conversaoDolar.html')


@app.route('/USD', methods=['GET','POST'])
def dolar():
    if request.method == 'POST':
        data = date.today().strftime("%m-%d-%Y")

        with urlopen(f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27USD%27&@dataCotacao=%27{data}%27&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda') as query:
            dados = json.load(query)
            
        real_dolar = round(float(request.form['real-dolar']) / float(dados['value'][0]['cotacaoCompra']), 2)
        dolar_real = round(float(request.form['dolar-real']) * float(dados['value'][0]['cotacaoVenda']), 2)
    
        return render_template('conversaoDolar.html',real_dolar=real_dolar, dolar_real=dolar_real)
    else:
        return render_template('index.html')


#EUR:
@app.route('/respostaEUR', methods=['GET','POST'])
def conversorEUR():
    if request.method == 'POST':
        return render_template('conversaoEuro.html')


@app.route('/EUR', methods=['GET','POST'])
def euro():
    if request.method == 'POST':
        data = date.today().strftime("%m-%d-%Y")

        with urlopen(f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27EUR%27&@dataCotacao=%27{data}%27&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda') as query:
            dados = json.load(query)
            
        real_euro = round(float(request.form['real-euro']) / float(dados['value'][0]['cotacaoCompra']), 2)
        euro_real = round(float(request.form['euro-real']) * float(dados['value'][0]['cotacaoVenda']), 2)
    
        return render_template('conversaoEuro.html',real_euro=real_euro, euro_real=euro_real)
    else:
        return render_template('index.html')  


#GBP:
@app.route('/respostaGBP', methods=['GET','POST'])
def conversorGBP():
    if request.method == 'POST':
        return render_template('conversaoLibra.html')


@app.route('/GBP', methods=['GET','POST'])
def libra():
    if request.method == 'POST':
        data = date.today().strftime("%m-%d-%Y")

        with urlopen(f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27GBP%27&@dataCotacao=%27{data}%27&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda') as query:
            dados = json.load(query)
            
        real_libra = round(float(request.form['real-libra']) / float(dados['value'][0]['cotacaoCompra']), 2)
        libra_real = round(float(request.form['libra-real']) * float(dados['value'][0]['cotacaoVenda']), 2)
    
        return render_template('conversaoLibra.html',real_libra=real_libra, libra_real=libra_real)
    else:
        return render_template('index.html')


app.run()