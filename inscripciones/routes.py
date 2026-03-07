from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Inscripciones, Alumnos, Curso, Maestros

inscripciones = Blueprint("inscripciones", __name__)


@inscripciones.route("/inscripciones")
def index():
    alumno_id = request.args.get("alumno_id", type=int)

    alumno = Alumnos.query.get_or_404(alumno_id)

    inscripciones_lista = db.session.query(
        Inscripciones, Alumnos, Curso, Maestros
    ).join(
        Alumnos, Inscripciones.alumno_id == Alumnos.id
    ).join(
        Curso, Inscripciones.curso_id == Curso.id
    ).join(
        Maestros, Curso.maestro_id == Maestros.matricula
    ).filter(
        Inscripciones.alumno_id == alumno_id
    ).all()

    subquery_cursos_inscritos = db.session.query(
        Inscripciones.curso_id
    ).filter(
        Inscripciones.alumno_id == alumno_id
    )

    cursos_disponibles = db.session.query(
        Curso, Maestros
    ).join(
        Maestros, Curso.maestro_id == Maestros.matricula
    ).filter(
        ~Curso.id.in_(subquery_cursos_inscritos)
    ).all()

    return render_template(
        "Alumnos/inscripciones.html",
        alumno_actual=alumno,
        inscripciones=inscripciones_lista,
        cursos_disponibles=cursos_disponibles
    )

@inscripciones.route("/quitar")
def quitar_inscripcion():
    id = request.args.get("id", type=int)
    alumno_id = request.args.get("alumno_id", type=int)

    inscripcion = Inscripciones.query.get_or_404(id)

    db.session.delete(inscripcion)
    db.session.commit()
    flash("Inscripción eliminada correctamente")

    return redirect(url_for("inscripciones.index", alumno_id=alumno_id))

@inscripciones.route("/inscribir")
def inscribir_curso():
    alumno_id = request.args.get("alumno_id", type=int)
    curso_id = request.args.get("curso_id", type=int)

    if not alumno_id or not curso_id:
        flash("Faltan datos para realizar la inscripción")
        return redirect(url_for("inscripciones.index", alumno_id=alumno_id))

    existe = Inscripciones.query.filter_by(
        alumno_id=alumno_id,
        curso_id=curso_id
    ).first()

    if existe:
        flash("Ese alumno ya está inscrito en ese curso")
        return redirect(url_for("inscripciones.index", alumno_id=alumno_id))

    nueva = Inscripciones(
        alumno_id=alumno_id,
        curso_id=curso_id
    )

    db.session.add(nueva)
    db.session.commit()
    flash("Inscripción realizada correctamente")

    return redirect(url_for("inscripciones.index", alumno_id=alumno_id))