import os

from flask import Flask
from flask_restful import Api
from . import db

# Modules
from .modules.PingPong import PingPong
from .modules.Register import Register
from .modules.Login import Login
from .modules.UploadImages import UploadImages
from .modules.DownloadImages import DownloadImages

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'serverside.sqlite'),
        UPLOAD_FOLDER='uploads'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent = True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Database initialising
    db.init_app(app)

    # API initialising
    api = Api(app)
    api.add_resource(PingPong, '/ping')
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(UploadImages, '/upload')
    api.add_resource(
        DownloadImages,
        '/viewall',
        endpoint = 'viewall',
        methods = ['GET']
    )
    api.add_resource(
        DownloadImages, 
        '/passphrase',
        endpoint = 'passphrase',
        methods = ['GET']
    )
    return app
