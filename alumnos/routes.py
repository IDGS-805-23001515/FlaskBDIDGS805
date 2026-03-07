from flask import Blueprint, render_template, request, redirect, url_for
from forms import AlumnoForm
from models import db, Alumnos

alumnos = Blueprint("alumnos", __name__)


@alumnos.route("/", methods=["GET", "POST"])
@alumnos.route("/index")
def index():
    create_form = AlumnoForm(request.form)
    alumno = Alumnos.query.all()
    return render_template("Alumnos/index.html", form=create_form, alumno=alumno)


@alumnos.route("/Alumnos", methods=["GET", "POST"])
def crear_alumno():
    create_form = AlumnoForm(request.form)
    if request.method == "POST":
        alumn = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.email.data,
            telefono=create_form.telefono.data
        )
        db.session.add(alumn)
        db.session.commit()
        return redirect(url_for("alumnos.index"))
    return render_template("Alumnos/Alumnos.html", form=create_form)

@alumnos.route("/detalles", methods=["GET"])
def detalles():
    id = request.args.get("id")
    alum1 = Alumnos.query.get_or_404(id)
    return render_template(
        "Alumnos/detalles.html",
        id=id,
        nombre=alum1.nombre,
        apellidos=alum1.apellidos,
        email=alum1.email,
        telefono=alum1.telefono
    )

@alumnos.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = AlumnoForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        alum1 = Alumnos.query.get_or_404(id)
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono
        return render_template("Alumnos/modificar.html", form=create_form, id=id)

    id = create_form.id.data
    alumn = Alumnos.query.get_or_404(id)
    alumn.nombre = create_form.nombre.data
    alumn.apellidos = create_form.apellidos.data
    alumn.email = create_form.email.data
    alumn.telefono = create_form.telefono.data
    db.session.commit()
    return redirect(url_for("alumnos.index"))

@alumnos.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = AlumnoForm(request.form)

    if request.method == "GET":
        id = request.args.get("id", type=int)
        alum1 = Alumnos.query.get_or_404(id)

        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono

        return render_template("Alumnos/eliminar.html", form=create_form, id=id)


    id = request.form.get("id", type=int) or create_form.id.data
    alum = Alumnos.query.get_or_404(id)

    db.session.delete(alum)
    db.session.commit()
    return redirect(url_for("alumnos.index"))