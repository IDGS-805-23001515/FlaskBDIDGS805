from flask import flash
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
import forms

from models import db, Alumnos
    
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
migrate=Migrate(app,db)
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
        apellidos=create_form.apellidos.data,
        telefono=create_form.telefono.data,
        email=create_form.email.data)
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("Alumnos.html",form=create_form)

@app.route("/detalles", methods=['GET','POST'])
def func():
    if request.method== 'GET':
        id=request.args.get('id')
        #select * from alumnos where id=id
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        nombre=alum1.nombre
        apellidos=alum1.apellidos
        telefono=alum1.telefono
        email=alum1.email
    return render_template('detalles.html',id=id,nombre=nombre,apellidos=apellidos,email=email, telefono=telefono)

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.USerForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        # select * from alumnos where id=id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.telefono.data = alum1.telefono
        create_form.email.data = alum1.email
    if request.method == 'POST':
        id= create_form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_form.nombre.data
        alum.apellidos=create_form.apellidos.data
        alum.telefono=create_form.telefono.data
        alum.email=create_form.email.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("modificar.html", form=create_form)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.USerForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        # select * from alumnos where id=id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.telefono.data = alum1.telefono
        create_form.email.data = alum1.email
    if request.method == 'POST':
        id= create_form.id.data
        alum=Alumnos.query.get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("eliminar.html", form=create_form)



    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()