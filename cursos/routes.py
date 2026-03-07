from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import CursoForm
from models import db, Curso, Maestros, Inscripciones
from flask import abort

cursos = Blueprint("cursos", __name__)


cursos.route("/", methods=["GET", "POST"])
@cursos.route("/curso", methods=["GET", "POST"])
def index():
    form = CursoForm(request.form)
    maestros = Maestros.query.all()
    form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros
    ]
    cursos_lista = db.session.query(Curso, Maestros).join(
    Maestros, Curso.maestro_id == Maestros.matricula
    ).all()
    return render_template("cursos/curso.html", form=form, curso=cursos_lista)


@cursos.route("/cursos", methods=["GET", "POST"])
def añadir_curso():
    create_form = CursoForm(request.form)


    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros
    ]

    if request.method == "POST" and create_form.validate():
        curs = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )
        db.session.add(curs)
        db.session.commit()
        return redirect(url_for("cursos.index"))

    return render_template("cursos/agregar.html", form=create_form)

@cursos.route("/curso/detalles", methods=["GET"])
def detalles():
    id = request.args.get("id", type=int)
    curso = Curso.query.get_or_404(id)

    maestro = Maestros.query.get(curso.maestro_id)  # o get_or_404 si siempre debe existir

    return render_template(
        "cursos/detalles.html",
        curso=curso,
        maestro=maestro
    )


@cursos.route("/curso/modificar", methods=["GET", "POST"])
def modificar():
    form = CursoForm(request.form)

    maestros = Maestros.query.all()
    form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros
    ]

    if request.method == "GET":
        id = request.args.get("id", type=int)
        curso = Curso.query.get_or_404(id)

        form.id.data = curso.id
        form.nombre.data = curso.nombre
        form.descripcion.data = curso.descripcion
        form.maestro_id.data = curso.maestro_id  # debe coincidir con el tipo de choice

    if request.method == "POST":
        id = form.id.data
        curso = Curso.query.get_or_404(id)

        curso.nombre = form.nombre.data
        curso.descripcion = form.descripcion.data
        curso.maestro_id = form.maestro_id.data  # sale del SelectField

        db.session.commit()
        return redirect(url_for("cursos.index"))

    return render_template("cursos/modificar.html", form=form)


@cursos.route("/curso/eliminar", methods=["GET", "POST"])
def eliminar_curso():
    form = CursoForm(request.form)

    maestros = Maestros.query.all()
    form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros
    ]

    if request.method == "GET":
        id = request.args.get("id", type=int)
        curso = Curso.query.get_or_404(id)

        form.id.data = curso.id
        form.nombre.data = curso.nombre
        form.descripcion.data = curso.descripcion
        form.maestro_id.data = curso.maestro_id

    if request.method == "POST":
        id = form.id.data
        curso = Curso.query.get_or_404(id)

        inscripciones = Inscripciones.query.filter_by(curso_id=id).count()

        if inscripciones > 0:
            flash("No se puede eliminar el curso porque tiene alumnos inscritos.", "warning")
            return redirect(url_for("cursos.index"))

        db.session.delete(curso)
        db.session.commit()
        flash("Curso eliminado correctamente.", "success")
        return redirect(url_for("cursos.index"))

    return render_template("cursos/eliminar.html", form=form)