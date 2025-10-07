from flask import Flask
from flasgger import Swagger
import pandas as pd

# Importa os blueprints
from app.controllers.series_controller import series_bp
from app.controllers.filtro_controller import filtro_bp

# DataFrame global
df = pd.read_csv('app/data/series.csv')

def create_app():
    app = Flask(__name__)
    Swagger(app)

    # Registro dos blueprints
    app.register_blueprint(series_bp)
    app.register_blueprint(filtro_bp)

    # Disponibiliza o DataFrame no contexto do app
    app.df = df

    # Salva o path do database
    app.config["DATA_PATH"] = 'app/data/series.csv'

    return app
