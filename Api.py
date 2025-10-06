from flask import Flask, request, abort, make_response, jsonify
import pandas as pd
from dataclasses import dataclass, asdict
from flasgger import Swagger
import json
from dataclasses import dataclass


@dataclass
class Ator:
    nome: str
    papel: str
    n_ep: int

    def to_dict(self):
        return {
            "nome": self.nome,
            "personagem": self.papel,
            "quantidade_episodios": self.n_ep
        }


@dataclass
class Serie:
    nome: str
    ordem: int
    ano_estreia: int
    ano_encerramento: int
    episodios: int
    faixa_etaria: int  # Pode ser número ou "Livre" == 0
    avaliacao: float
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
        nome=row['titulo'],
        ordem=row['ordem'],
        ano_estreia=row['ano_estreia'],
        ano_encerramento=row['ano_encerramento'],
        episodios=row['episodios'],
        faixa_etaria=row['classificacao_indicativa'],
        avaliacao=row['nota_imdb'],
        link=row['link'],
        popularidade=row['popularidade'],
        atores=[]

    )
    for row in df.to_dict(orient="records")
]


@app.route("/series/")
def series():
    """
    Lista as séries disponíveis
    ---
    tags:
      - Séries
    description: Retorna uma lista das 200 primeiras séries cadastradas.
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
    return jsonify([asdict(p) for p in lista_links[0:200]]), 200


@app.route("/series/<int:id>/", methods=["GET"])
def series_by_id(id):
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
    pessoa_encontrada = next((p for p in lista_links if p.ordem == id), None)

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