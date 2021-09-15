from flask import Blueprint
from flask_restx import Api
from .client_namespace import client_ns
from .report_namespace import report_ns

v1_bp = Blueprint(
    'v1', __name__
)
api = Api(v1_bp, doc='/docs')

api.add_namespace(client_ns)
api.add_namespace(report_ns)

