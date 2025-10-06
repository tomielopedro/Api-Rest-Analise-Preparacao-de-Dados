from flask import Blueprint, jsonify, make_response, current_app
from dataclasses import asdict
from app.models.serie import Serie

series_bp = Blueprint('series', __name__)

@series_bp.route("/series/<int:qtd>/", methods=["GET"])
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
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: "Breaking Bad"
              ordem:
                type: integer
                example: 1
              ano_estreia:
                type: integer
                example: 2008
              ano_encerramento:
                type: integer
                example: 2013
              episodios:
                type: integer
                example: 62
              classificacao_indicativa:
                type: integer
                example: 18
              nota_imdb:
                type: number
                format: float
                example: 9.5
              link:
                type: string
                example: "https://www.imdb.com/title/tt0903747/"
              popularidade:
                type: number
                format: float
                example: 98.5
              atores:
                type: array
                items:
                  type: string
                example: ["Bryan Cranston", "Aaron Paul"]
    """
    df = current_app.df
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
            atores=row.get('atores', [])
        )
        for row in df.to_dict(orient="records")
    ]
    return jsonify([asdict(p) for p in lista_links[:qtd]]), 200


@series_bp.route("/series-id/<int:id>/", methods=["GET"])
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
        description: ID da série a ser retornada
    responses:
      200:
        description: Série encontrada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: "Breaking Bad"
            ordem:
              type: integer
              example: 1
            ano_estreia:
              type: integer
              example: 2008
            ano_encerramento:
              type: integer
              example: 2013
            episodios:
              type: integer
              example: 62
            classificacao_indicativa:
              type: integer
              example: 18
            nota_imdb:
              type: number
              format: float
              example: 9.5
            link:
              type: string
              example: "https://www.imdb.com/title/tt0903747/"
            popularidade:
              type: number
              format: float
              example: 98.5
            atores:
              type: array
              items:
                type: string
              example: ["Bryan Cranston", "Aaron Paul"]
      404:
        description: Série não encontrada
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Série não encontrada"
    """
    df = current_app.df
    row = df.loc[df["id"] == id]

    if not row.empty:
        serie = row.to_dict(orient="records")[0]
        return jsonify(serie), 200
    else:
        return make_response(jsonify({"erro": "Série não encontrada"}), 404)
