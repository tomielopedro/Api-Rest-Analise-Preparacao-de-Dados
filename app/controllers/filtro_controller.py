from flask import Blueprint, jsonify, request, current_app

filtro_bp = Blueprint('filtro', __name__)

@filtro_bp.route('/filtro', methods=['POST'])
def filtro_series():
    """
    Filtra séries com base em um ou mais campos enviados via JSON.
    ---
    tags:
      - Filtros
    consumes:
      - application/json
    parameters:
      - in: body
        name: filtros
        description: Campos para filtrar as séries. Cada campo é opcional.
        required: true
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            titulo:
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
    responses:
      200:
        description: Lista de séries filtradas ou mensagem caso nenhum registro seja encontrado
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              titulo:
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
      400:
        description: Erro em caso de JSON inválido ou campos incorretos
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Campos inválidos: campoX"
    """
    df = current_app.df
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Nenhum JSON foi enviado"}), 400

    campos_invalidos = [campo for campo in data.keys() if campo not in df.columns]
    if campos_invalidos:
        return jsonify({"erro": f"Campos inválidos: {', '.join(campos_invalidos)}"}), 400

    resultado = df.copy()
    for campo, valor in data.items():
        resultado = resultado[resultado[campo] == valor]

    if resultado.empty:
        return jsonify({"mensagem": "Nenhum registro encontrado para os filtros informados."}), 200

    return jsonify(resultado.to_dict(orient="records")), 200
