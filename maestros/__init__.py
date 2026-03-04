from flask import Blueprint

maestros = Blueprint(
    'maestros',
    __name__,
    template_folder='templates'
)

from . import routes
