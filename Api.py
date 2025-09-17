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

@app.route("/wikipedia_links/", defaults={"id": None}, methods=["GET"])
@app.route("/wikipedia_links/<int:id>", methods=["GET"])
def wikipedia_links(id):
    """
    Retorna informações sobre pessoas cadastradas no sistema.

    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: false
        description: ID da pessoa (se não informado, retorna 200 pessoas)
    responses:
      200:
        description: Retorna a(s) pessoa(s) encontrada(s)
        schema:
          type: object
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
    # Se nenhum ID for fornecido, retorna a lista completa
    if id is None:
        return jsonify([asdict(p) for p in lista_pessoas[0:200]]), 200

    # Busca pessoa pelo ID
    pessoa_encontrada = next((p for p in lista_pessoas if p.id == id), None)

    if pessoa_encontrada:
        return jsonify(asdict(pessoa_encontrada)), 200
    else:
        return make_response(jsonify({"erro": "Pessoa não encontrada"}), 404)




if __name__ == "__main__":
    app.run(debug=True)