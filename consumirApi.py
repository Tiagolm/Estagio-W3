from urllib.request import urlopen
import json
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("inputExemplo.html")


@app.route('/servicos', methods=["POST", "GET"])
def resposta():
    servico = request.form["servico"]
    with urlopen(
            "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifaPorValores/versao/v1/odata/ListaTarifasPorValores(CodigoGrupoConsolidado=@CodigoGrupoConsolidado,CodigoServico=@CodigoServico)?@CodigoGrupoConsolidado='03'&@CodigoServico='{}'&$top=1000&$format=json".format(
                    servico)) as listaTed:
        dados = json.load(listaTed)

    return render_template("Servico.html", dados=dados)


app.run()
