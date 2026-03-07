from wtforms import Form
from wtforms import IntegerField, StringField,  EmailField, SelectField
from wtforms import validators

class AlumnoForm(Form):

    id = IntegerField("Id")

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=20)
    ])

    apellidos = StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=20)
    ])

    email = EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese correo válido")
    ])

    telefono = StringField("Teléfono", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=10, max=10)
    ])

class MaestroForm(Form):

    matricula = IntegerField("Matricula")

    nombre = StringField("Nombre", [
        validators.DataRequired(),
        validators.Length(min=4, max=20)
    ])

    apellidos = StringField("Apellidos", [
        validators.DataRequired(),
        validators.Length(min=4, max=20)
    ])

    email = EmailField("Correo", [
        validators.DataRequired(),
        validators.Email()
    ])

    especialidad = StringField("Especialidad", [
        validators.DataRequired(),
        validators.Length(min=4, max=50)
    ])

class CursoForm(Form):

    id = IntegerField("ID")

    nombre = StringField("Nombre", [
        validators.DataRequired(),
        validators.Length(min=4, max=150)
    ])

    descripcion = StringField("Descripcion", [
        validators.DataRequired(),
        validators.Length(min=4, max=150)
    ])

    maestro_id = SelectField(
        "Maestro",
        coerce=int,
        validators=[validators.DataRequired()]
    )

class InscripcionForm(Form):

    alumno_id = SelectField(
        "Alumno",
        coerce=int,
        validators=[validators.DataRequired()]
    )

    curso_id = SelectField(
        "Curso",
        coerce=int,
        validators=[validators.DataRequired()]
    )