from flask import Flask, render_template, request
from static.plt.graph import build_graph
from urllib.request import urlopen
import matplotlib.pyplot as plt
import csv
import json

app = Flask(__name__)

listaNomeBancos = []
listaTaxaBancos = []


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




@app.route('/servisos')
def tarifas():
    return render_template("servico.html")



@app.route('/respostaServicos', methods=["POST", "GET"])
def tarifasResposta():
    servico = request.form["servico"]
    with urlopen(
            "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifaPorValores/versao/v1/odata/ListaTarifasPorValores(CodigoGrupoConsolidado=@CodigoGrupoConsolidado,CodigoServico=@CodigoServico)?@CodigoGrupoConsolidado='03'&@CodigoServico='{}'&$top=1000&$format=json".format(
                    servico)) as listaTed:
        dados = json.load(listaTed)

    return render_template("respostaServico.html", dados=dados)




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
        valor = request.form['valor']

        i = 0
        for item in listaNomeBancos:
            if item == nomeBanco:
                return render_template('respostaSimulador.html', resultado=str(float(valor) * float(listaTaxaBancos[i]))) 
            else:
                i = i + 1




@app.route('/grafico')
def opcoes():

    with open('static/2018-1_CA.csv', encoding='iso-8859-1') as query:
        data = csv.reader(query, delimiter='\t')
        
        lista_de_postos = []
        postos_guradados = ""

        for linha in data:
            nova_linha = linha[0].split('  ')

            if postos_guradados != nova_linha[2]:
                postos_guradados = nova_linha[2]
                if postos_guradados not in lista_de_postos:
                    lista_de_postos.append(nova_linha[2])
         
    return render_template('combustivel.html',postos=lista_de_postos)


@app.route('/respostaGrafico', methods=['POST'])
def grafico():
    precos_combustiveis = []
    datas_combustiveis = []

    with open('static/2018-1_CA.csv', encoding='iso-8859-1') as query:
        data = csv.reader(query, delimiter='\t')

        posto = request.form['postos']
        combustivel = request.form['combustiveis']


        for linha in data:
            nova_linha = linha[0].split('  ')                        

            if nova_linha[2] == posto:
                if nova_linha[5] == combustivel or nova_linha[5] == combustivel + " S10":

                    precos_combustiveis.append(float(nova_linha[7].replace(',','.')))
                    datas_combustiveis.append(nova_linha[6])

    grafico_1 = build_graph(datas_combustiveis, precos_combustiveis, 'ro',"dias (30)","preço (R$)","Evolução do preço")

    return render_template('respostaCombustivel.html', grafico=grafico_1)




@app.route('/conversor')
def conversor():
    return render_template('conversor.html')


#USD
@app.route('/respostaUSD', methods=['GET','POST'])
def conversorUSD():
    if request.method == 'POST':
        return render_template('conversaoDolar.html')

@app.route('/USD', methods=['GET','POST'])
def Dolar():
    if request.method == 'POST':
        data = request.form['data'].split('/')
        data = data[1] + "-" + data[0] + "-" + data[2]

        with urlopen(f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27USD%27&@dataCotacao=%27{data}%27&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda') as query:
            dados = json.load(query)

        if request.form['lista'] == 'converter':
            
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
def Euro():
    if request.method == 'POST':
        data = request.form['data'].split('/')
        data = data[1] + "-" + data[0] + "-" + data[2]

        with urlopen(f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27EUR%27&@dataCotacao=%27{data}%27&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda') as query:
            dados = json.load(query)

        if request.form['lista'] == 'ver_conversao':
            
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
def Libra():
    if request.method == 'POST':
        data = request.form['data'].split('/')
        data = data[1] + "-" + data[0] + "-" + data[2]

        with urlopen(f'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27GBP%27&@dataCotacao=%27{data}%27&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda') as query:
            dados = json.load(query)

        if request.form['lista'] == 'ver_conversao':
            
          real_libra = round(float(request.form['real-libra']) / float(dados['value'][0]['cotacaoCompra']), 2)
          libra_real = round(float(request.form['libra-real']) * float(dados['value'][0]['cotacaoVenda']), 2)
    
        return render_template('conversaoLibra.html',real_libra=real_libra, libra_real=libra_real)
    else:
        return render_template('index.html')

app.run()