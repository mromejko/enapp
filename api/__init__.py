from flask import Flask
from config import Config, EXTENSIONS
from .helpers import get_commands, get_extensions
from .logger import logger
import sys

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register extensions
    extensions = dict(get_extensions(EXTENSIONS))
    register_extensions(app, extensions)

    with app.app_context():

        from api.v1 import v1_bp
        app.register_blueprint(v1_bp, url_prefix="/v1")

        register_cli_commands(app)

        return app

import api.models

def register_cli_commands(app):
    commands = list(get_commands())
    for name, command in commands:
        if name in app.cli.commands:
            logger.error(f"Command with name {name} already exists!")
            sys.exit(1)
        app.cli.add_command(command)

def register_extensions(app, extensions):
    for extension in extensions.values():
        extension.init_app(app)