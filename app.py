from flask import Flask, render_template, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
from maestros.routes import maestros
from alumnos.routes import alumnos
from cursos.routes import cursos
from inscripciones.routes import inscripciones
from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(alumnos)   
app.register_blueprint(maestros)
app.register_blueprint(cursos)
app.register_blueprint(inscripciones)
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()