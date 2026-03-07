from forms import MaestroForm
from models import db, Maestros, Alumnos, Inscripciones
from . import maestros
from cursos.routes import Curso
from flask import Blueprint, render_template, request, redirect, url_for

alumnos = Blueprint("maestros", __name__)

@maestros.route("/maestros", methods=["GET", "POST"])
def listado():
    create_form = MaestroForm(request.form)
    maestros = Maestros.query.all()
    return render_template(
        "maestros/listadoMaes.html",
        form=create_form,
        maestros=maestros
    )

@maestros.route("/maestros/insertar", methods=["GET", "POST"])
def insertar():
    create_form = MaestroForm(request.form)
    if request.method == "POST":
        master=Maestros(nombre=create_form.nombre.data,
                    apellidos=create_form.apellidos.data,
                    especialidad=create_form.especialidad.data,
                    email=create_form.email.data
                    )
        db.session.add(master)
        db.session.commit()
        return redirect(url_for("maestros.listado"))
    return render_template("maestros/insertar.html", form=create_form)

@maestros.route("/maestros/detalles", methods=["GET", "POST"])
def detalles():
    if request.method == "GET":
        matricula = request.args.get('matricula')
        maester = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        nombre = maester.nombre
        apellidos = maester.apellidos
        especialidad = maester.especialidad
        email = maester.email        
    return render_template("maestros/detalles.html", matricula=matricula, nombre=nombre, apellidos=apellidos,email=email, especialidad=especialidad)


@maestros.route("/maestros/modificar", methods=["GET", "POST"])
def modificar():
    create_form = MaestroForm(request.form)
    if request.method == "GET":
        matricula = request.args.get('matricula')
        maester = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        create_form.matricula.data = maester.matricula 
        create_form.nombre.data = maester.nombre
        create_form.apellidos.data = maester.apellidos
        create_form.email.data = maester.email
        create_form.especialidad.data = maester.especialidad
    if request.method == "POST":
        matricula = create_form.matricula.data
        master = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        master.nombre = create_form.nombre.data
        master.apellidos = create_form.apellidos.data
        master.email = create_form.email.data        
        master.especialidad = create_form.especialidad.data        
        db.session.add(master)
        db.session.commit()
        return redirect(url_for("maestros.listado"))
    return render_template("maestros/modificar.html", form=create_form, matricula=matricula)

@maestros.route("/maestros/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = MaestroForm(request.form)
    if request.method == "GET":
        matricula = request.args.get('matricula')
        maester = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        create_form.matricula.data = maester.matricula 
        create_form.nombre.data = maester.nombre
        create_form.apellidos.data = maester.apellidos
        create_form.email.data = maester.email
        create_form.especialidad.data = maester.especialidad
    if request.method == "POST":
        matricula = create_form.matricula.data
        master = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        db.session.delete(master)
        db.session.commit()
        return redirect(url_for("maestros.listado"))
    return render_template("maestros/eliminar.html", form=create_form, matricula=matricula)

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"

@maestros.route("/maestros/cursos")
def cursos_maestro():
    maestro_id = request.args.get("maestro_id", type=int)

    maestro = Maestros.query.get_or_404(maestro_id)

    resultados = db.session.query(
        Curso, Alumnos
    ).join(
        Inscripciones, Curso.id == Inscripciones.curso_id
    ).join(
        Alumnos, Inscripciones.alumno_id == Alumnos.id
    ).filter(
        Curso.maestro_id == maestro_id
    ).all()

    cursos_dict = {}

    for curso, alumno in resultados:
        if curso.id not in cursos_dict:
            cursos_dict[curso.id] = {
                "curso": curso,
                "alumnos": []
            }
        cursos_dict[curso.id]["alumnos"].append(alumno)

    return render_template(
        "maestros/cursos_maestro.html",
        maestro=maestro,
        cursos_dict=cursos_dict
    )