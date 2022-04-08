from flask import Flask
import json

def create_app(config_name):
    app = Flask(__name__)

    with open('waccess.json') as arch:
        config = json.load(arch)
    conection = 'postgresql://' + config['user']+ ':' + config['password'] + '@' + config['host'] + ':' + str(config['port']) + '/' + config['database']
    app.config['SQLALCHEMY_DATABASE_URI'] = conection
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app

