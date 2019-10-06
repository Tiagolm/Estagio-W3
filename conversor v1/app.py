from flask import Flask, render_template, request
from urllib.request import urlopen
import json

app = Flask(__name__)

#raiz:
@app.route('/')
def hello():
    return render_template('index.html')



#-USD:
@app.route('/conversorUSD', methods=['GET','POST'])
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

        if request.form['lista'] == 'ver_conversao':
            
          real_dolar = round(float(request.form['real-dolar']) / float(dados['value'][0]['cotacaoCompra']), 2)
          dolar_real = round(float(request.form['dolar-real']) * float(dados['value'][0]['cotacaoVenda']), 2)
    
        return render_template('conversaoDolar.html',real_dolar=real_dolar, dolar_real=dolar_real)
    else:
        return render_template('index.html')



#-EUR:
@app.route('/conversorEUR', methods=['GET','POST'])
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
@app.route('/conversorGBP', methods=['GET','POST'])
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