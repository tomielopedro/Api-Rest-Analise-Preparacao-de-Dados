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
lista_links = [
    Pessoa(
        id=row["id"],
        link=row["link"],
        nome=row["nome"],
        eh_pessoa=bool(row["eh_pessoa"]),
        probabilidade=row["probabilidade"],
    )
    for row in df.to_dict(orient="records")
]

@app.route("/wikipedia_links/", defaults={"id": None}, methods=["GET"])
@app.route("/wikipedia_links/<int:id>/", methods=["GET"])
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
        return jsonify([asdict(p) for p in lista_links[0:200]]), 200

    # Busca pessoa pelo ID
    pessoa_encontrada = next((p for p in lista_links if p.id == id), None)

    if pessoa_encontrada:
        return jsonify(asdict(pessoa_encontrada)), 200
    else:
        return make_response(jsonify({"erro": "Pessoa não encontrada"}), 404)


@app.route("/wikipedia_test", methods=["GET"])
def wikipedia_test():
    """
    Testa parâmetro de query no Wikipedia
    ---
    parameters:
      - name: only_pessoa
        in: query
        type: boolean
        required: false
        description: Indica se a lista retornada é apenas de pessoas
    responses:
      200:
        description: Retorna a lista filtrada
        schema:
          type: array
          items:
            type: object
    """
    only_pessoa_str = request.args.get("only_pessoa")

    # Converte string para boolean (true/1/t/yes → True)
    only_pessoa = (
        only_pessoa_str and only_pessoa_str.lower() in ["true", "1", "t", "yes", "y"]
    )

    if only_pessoa:
        print(lista_links)
        lista_pessoas = list(filter(lambda x: x.eh_pessoa, lista_links))
        print(lista_pessoas)
        return jsonify([asdict(p) for p in lista_links if p.eh_pessoa]), 200

    return jsonify([asdict(p) for p in lista_links]), 200



if __name__ == "__main__":
    app.run(debug=True)