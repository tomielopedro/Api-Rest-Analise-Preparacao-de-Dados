from flask import Flask, request, abort, make_response, jsonify
import pandas as pd
from dataclasses import dataclass, asdict
from flasgger import Swagger
import json


@dataclass
class Pessoa:
    id:int
    link: str
    nome: str
    eh_pessoa: bool
    probabilidade: float

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

app = Flask(__name__)
swagger = Swagger(app)


df = pd.read_csv('data/resultado_links.csv')
lista_pessoas = [Pessoa(**row) for row in df.to_dict(orient="records")]

@app.route("/wikipedia_links/", methods=['GET'])
@app.route("/wikipedia_links/<int:id>", methods=['GET'])
def wikipedia_link(id):
    """
    Retorna uma pessoa pelo id
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da pessoa
    responses:
      200:
        description: Retorna a pessoa encontrada
        schema:
          id: Pessoa
          properties:
            id:
              type: integer
            nome:
              type: string
            link:
              type: string
            eh_pessoa:
              type: boolean
            probabilidade:
              type: number
      404:
        description: Pessoa não encontrada
    """
    pessoa_encontrada = next((p for p in lista_pessoas if p.id == id), None)
    if pessoa_encontrada:
        return jsonify(asdict(pessoa_encontrada))
    else:
        return make_response(jsonify({"erro": "Pessoa não encontrada"}), 404)


@app.route("/wikipedi_links", methods=['GET', 'POST'])
def pessoas():
    """
    Retorna uma lista de pessoas de exemplo
    ---
    responses:
      200:
        description: Retorna um objeto Pessoa
        examples:
          application/json:
            nome: "Ana"
            link: "http://pessoas"
            eh_pessoa: true
            probabilidade: 0.95
    """
    if request.method == "GET":
        return make_response(jsonify(lista_pessoas))
    """elif request.method == "POST":
        # Incluir uma nova tarefa
        dados = request.get_json()
        nova_tarefa = dados["tarefa"]
        if nova_tarefa not in lista_pessoas:
            lista_pessoas.append(nova_tarefa)
            return make_response(jsonify("Tarefa foi incluída com sucesso"), 200)
        else:
            return make_response(jsonify("A tarefa já existe"), 400)"""
"""
@app.route("/tarefa/<int:id>", methods=["GET", "PUT", "DELETE"])
def tarefa(id):
    if id >= len(lista_tarefas):
        return make_response(jsonify("Tarefa inexistente"), 400)
    else:
        if request.method == "GET":
            # Retornar uma tarefa
            return make_response(jsonify(lista_tarefas[id]))
        elif request.method == "PUT":
            # Editar uma tarefa
            dados = request.get_json()
            tarefa_editada = dados["tarefa"]
            lista_tarefas[id] = tarefa_editada
            return make_response(jsonify("Tarefa editada com sucesso"), 200)
        elif request.method == "DELETE":
            # Apagar uma tarefa
            lista_tarefas.pop(id)
            return make_response(jsonify("Tarefa excluída com sucesso"), 200)
        else:
            abort(404)
"""
if __name__ == "__main__":
    app.run(debug=True)