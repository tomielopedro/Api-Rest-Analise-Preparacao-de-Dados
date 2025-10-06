from flask import Flask, request, abort, make_response, jsonify
import pandas as pd
from dataclasses import asdict
from flasgger import Swagger
import json
from dataclasses import dataclass


@dataclass
class Serie:
    id: int
    nome: str
    ordem: int
    ano_estreia: int
    ano_encerramento: int
    episodios: int
    classificacao_indicativa: int  # Pode ser número ou "Livre" == 0
    nota_imdb: float
    link: str
    popularidade: float
    atores: list


    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

app = Flask(__name__)
swagger = Swagger(app)


df = pd.read_csv('data/series.csv')
lista_links = [
    Serie(
        id=row['id'],
        nome=row['titulo'],
        ordem=row['ordem'],
        ano_estreia=row['ano_estreia'],
        ano_encerramento=row['ano_encerramento'],
        episodios=row['episodios'],
        classificacao_indicativa=row['classificacao_indicativa'],
        nota_imdb=row['nota_imdb'],
        link=row['link'],
        popularidade=row['popularidade'],
        atores=[]

    )
    for row in df.to_dict(orient="records")
]


@app.route("/series/<int:qtd>/", methods=["GET"])
def series(qtd):
    """
    Lista uma quantidade específica de séries
    ---
    tags:
      - Séries
    parameters:
      - name: qtd
        in: path
        type: integer
        required: true
        description: Quantidade de séries a retornar
    responses:
      200:
        description: Lista de séries retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              ordem:
                type: integer
                example: 1
              nome:
                type: string
                example: "Pessoa 1"
    """
    return jsonify([asdict(p) for p in lista_links[0:qtd]]), 200

@app.route("/series-id/<int:id>/", methods=["GET"])
def get_series_by_id(id):
    """
    Retorna uma série específica pelo ID
    ---
    tags:
      - Séries
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da série
    responses:
      200:
        description: Série encontrada com sucesso
        schema:
          type: object
          properties:
            ordem:
              type: integer
              example: 1
            nome:
              type: string
              example: "Pessoa 1"
      404:
        description: Série não encontrada
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Pessoa não encontrada"
    """
    pessoa_encontrada = next((p for p in lista_links if p.id == id), None)

    if pessoa_encontrada:
        return jsonify(asdict(pessoa_encontrada)), 200
    else:
        return make_response(jsonify({"erro": "Pessoa não encontrada"}), 404)



@app.route('/filtro', methods=['POST'])
def receber_json():

    data = request.get_json()

    if not data:
        return jsonify({"erro": "Nenhum JSON foi enviado"}), 400

    nome = data.get('nome')
    idade = data.get('idade')

    # Faz algo com os dados
    resposta = {
        "mensagem": f"Olá, {nome}! Você tem {idade} anos."
    }

    return jsonify(resposta), 200


if __name__ == "__main__":
    app.run(debug=True)