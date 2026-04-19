from flask import Flask
from flask_cors import CORS
from prode.routes.partidos import partidos_bp
from prode.routes.predicciones import prediccion_bp
from prode.routes.usuarios import usuarios_bp
from prode.routes.ranking import ranking_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(partidos_bp, url_prefix="/partidos")
app.register_blueprint(prediccion_bp, url_prefix="/partidos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(ranking_bp, url_prefix="/ranking")


if __name__ == "__main__":
    app.run(port=5000, debug=True)