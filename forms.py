from wtforms import Form
from wtforms import IntegerField, StringField, PasswordField
from wtforms import EmailField
from wtforms import validators

class UserForm2(Form):
    id = IntegerField("Id")
    nombre=StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=4, max=10, message="Ingrese un valor valido")
    ])
    matricula = IntegerField("Matricula")
    nombre=StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=4, max=10, message="Ingrese un valor valido")
    ])
    apellidos=StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido")
    ])
    email=EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese correo válido")
    ])
    telefono=EmailField("Teléfono", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese correo válido")
    ])
    especialidad=EmailField("Especialidad", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese correo válido")
    ])