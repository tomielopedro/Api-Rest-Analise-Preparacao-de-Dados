import pandas as pd
from flask import Blueprint, jsonify, make_response, current_app, request
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


@series_bp.route("/series/", methods=["POST"])
def create_serie():
    """
    Cria uma nova série.
    ---
    tags:
      - Séries
    summary: Cria uma nova série no sistema.
    description: >
      Este endpoint cria uma nova série no banco de dados a partir dos dados fornecidos no corpo da requisição.
      Os campos `ano_encerramento` e `atores` são opcionais.
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: Objeto JSON contendo as informações da nova série.
        schema:
          type: object
          required:
            - nome
            - ordem
            - ano_estreia
            - episodios
            - classificacao_indicativa
            - nota_imdb
            - link
            - popularidade
          properties:
            nome:
              type: string
              description: Nome da série.
              example: "Breaking Bad"
            ordem:
              type: integer
              description: Ordem da série no catálogo.
              example: 1
            ano_estreia:
              type: integer
              description: Ano de estreia da série.
              example: 2008
            ano_encerramento:
              type: integer
              description: Ano em que a série foi encerrada (opcional).
              example: 2013
            episodios:
              type: integer
              description: Número total de episódios.
              example: 62
            classificacao_indicativa:
              type: integer
              description: Classificação indicativa de idade.
              example: 18
            nota_imdb:
              type: number
              format: float
              description: Nota da série no IMDb.
              example: 9.5
            link:
              type: string
              description: Link para a página da série no IMDb.
              example: "https://www.imdb.com/title/tt0903747/"
            popularidade:
              type: number
              format: float
              description: Índice de popularidade da série.
              example: 98.5
            atores:
              type: array
              items:
                type: string
              description: Lista de atores principais (opcional).
              example: "Bryan Cranston, Aaron Paul"
    responses:
      201:
        description: Série criada com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Série criada com sucesso"
            id:
              type: integer
              example: 10
      400:
        description: Requisição inválida (campos obrigatórios ausentes ou formato incorreto).
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Campos obrigatórios ausentes"
    """
    df = current_app.df
    data = request.get_json()

    campos_obrigatorios = [
        "nome", "ordem", "ano_estreia", "episodios", "classificacao_indicativa",
        "nota_imdb", "link", "popularidade",
    ]

    if not all(campo in data for campo in campos_obrigatorios):
        return make_response(jsonify({"erro": "Campos obrigatórios ausentes"}), 400)

    new_id = int(df["id"].max() + 1 if not df.empty else 1)
    nova_serie = Serie(id=new_id, **data)
    nova_linha = pd.DataFrame([asdict(nova_serie)])
    nova_linha = nova_linha.rename(columns={"nome": "titulo"})

    current_app.df = pd.concat([df, nova_linha], ignore_index=True)
    current_app.df.to_csv(current_app.config["DATA_PATH"], index=False)

    return jsonify({"mensagem": "Série criada com sucesso", "id": new_id}), 201


@series_bp.route("/series-id/<int:id>/", methods=["PUT"])
def update_serie(id):
    """
    Atualiza uma série existente pelo ID
    ---
    tags:
      - Séries
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da série a ser atualizada
      - in: body
        name: body
        required: true
        description: Campos a serem atualizados
        schema:
          type: object
          required:
            - nome
            - ordem
            - ano_estreia
            - episodios
            - classificacao_indicativa
            - nota_imdb
            - link
            - popularidade
          properties:
            nome:
              type: string
              description: Nome da série.
              example: "Breaking Bad"
            ordem:
              type: integer
              description: Ordem da série no catálogo.
              example: 1
            ano_estreia:
              type: integer
              description: Ano de estreia da série.
              example: 2008
            ano_encerramento:
              type: integer
              description: Ano em que a série foi encerrada (opcional).
              example: 2013
            episodios:
              type: integer
              description: Número total de episódios.
              example: 62
            classificacao_indicativa:
              type: integer
              description: Classificação indicativa de idade.
              example: 18
            nota_imdb:
              type: number
              format: float
              description: Nota da série no IMDb.
              example: 9.5
            link:
              type: string
              description: Link para a página da série no IMDb.
              example: "https://www.imdb.com/title/tt0903747/"
            popularidade:
              type: number
              format: float
              description: Índice de popularidade da série.
              example: 98.5
            atores:
              type: array
              items:
                type: string
              description: Lista de atores principais (opcional).
              example: "Bryan Cranston, Aaron Paul"
    responses:
      200:
        description: Série atualizada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Série atualizada com sucesso"
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
    df = df.rename(columns={"titulo": "nome"})
    data = request.get_json()

    if id not in df["id"].values:
        return make_response(jsonify({"erro": "Série não encontrada"}), 404)

    for key, value in data.items():
        if key in df.columns:
            df.loc[df["id"] == id, key] = value

    current_app.df = df.rename(columns={"nome": "titulo"})
    current_app.df.to_csv(current_app.config["DATA_PATH"], index=False)

    return jsonify({"mensagem": "Série atualizada com sucesso"}), 200


@series_bp.route("/series-id/<int:id>/", methods=["DELETE"])
def delete_serie(id):
    """
    Deleta uma série existente pelo ID
    ---
    tags:
      - Séries
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da série a ser deletada
    responses:
      200:
        description: Série deletada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Série com id 2 deletada com sucesso"
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

    if id not in df["id"].values:
        return make_response(jsonify({"erro": "Série não encontrada"}), 404)

    df = df[df["id"] != id]
    current_app.df = df.reset_index(drop=True)

    current_app.df.to_csv(current_app.config["DATA_PATH"], index=False)

    return jsonify({"mensagem": f"Série com id {id} deletada com sucesso"}), 200