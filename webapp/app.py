from flask import Flask, escape, request, render_template #,url_for
app = Flask(__name__)

#Hello world, introdução ao flask
@app.route('/')
def hello_world():
    return 'Hello, World!'




#URLs únicas
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'




#Variable Rules: Você pode adicionar uma seção de variável seguindo a sintaxe abaixo, lembrado que há mais opções além
#de "path" como <flutuante/float:<nome_qualquer>, <id/int:<nome_qualquer> e <user/<nome_qualquer> (default)
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html',name=name) 




#O parâmetro "methods" nos permite executar métodos com base no tipo de requisição feita para o nosso servidor; nesse
#exemplo, o método "do_the_login()" é executado toda vez que p usuário enviar informação para o servidor (POST), já o
#outro é executado quando outro método (no caso, o GET) é chamado. É necessário importar o módule 'request'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do_the_login()'
    else:
        return 'show_the_login_form()'


#Esses 2 routes() estão intimamente ligados; primeiramente no template form.html há um formulário ao qual possui 2
#inputs: Name e Note. As respostas desses inputs são recebidas nas variáveis "nome" e "nota" através da request.form[],
#e depois cuspidas para o o HTML "/response" (de uma maneira bem porca ainda)
@app.route('/form')
def form():
    return render_template('form.html') #retorna o template HTML

@app.route('/response', methods=['GET', 'POST'])
def response(): #função que será executada

    if request.method == 'POST':
        nome = request.form['fname']
        nota = request.form['note']

        #name=nome e note=nota --> Variáveis dentro do HTML recebendo as variáves python
        return render_template('response.html', name=nome, note=nota) 
    else:
        return "Digs é gay."




app.route('/params', methods=['GET', 'POST'])
def params():
    arg1 = str(request.args['arg1'])
    arg2 = str(request.args['arg2'])

    return 'Arg1: ' + arg1 + 'Arg2: ' + arg2


'''
DICA DE OURO: Algumas informações da documentação do flask estão desatualizadas e o miniframework é fortemente tipado,
oque faz com que até as PASTAS como a pasta 'templates' tenham que ter nomes expecíficos; por exemplo, se 'templates'
tiver outro nome, o flask não vai encontrar.
'''