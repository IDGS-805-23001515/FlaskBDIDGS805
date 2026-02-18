from flask import flash
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms

from models import db, Alumnos
    
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf=CSRFProtect(app)
    
@app.errorhandler(404)
def page_not_fount(e):
    return render_template ("404.html"), 404
    
@app.route("/", methods=['GET','POST'])
@app.route("/index")
def index():
    create_form=forms.USerForm2(request.form)
    alumno=Alumnos.query.all()
    return render_template("index.html",form=create_form,alumno=alumno)
    
    
@app.route("/Alumnos",methods=['GET','POST'])
def alumnos():
    create_form=forms.USerForm2(request.form)
    if request.method=='POST':
        alum=Alumnos(nombre=create_form.nombre.data,
        apaterno=create_form.apaterno.data,
        email=create_form.email.data)
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("Alumnos.html",form=create_form)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()