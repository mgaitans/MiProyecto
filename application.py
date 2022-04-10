from flask import Flask
from config import create_app
from modelos import db, Blacklists, BlacklistsSchema, App_uuid
from flask_restful import Api  
from vistas import VistaBlacklists, VistaBlacklist, VistaTokenacceso, Test
from flask_jwt_extended import JWTManager
import json

application = create_app('default')
app_context = application.app_context()
app_context.push()
db.init_app(application)
db.create_all()
api = Api(application)
api.add_resource(VistaBlacklists, '/blacklists')
api.add_resource(VistaBlacklist, '/blacklist/<email>') ##/blacklists/<string:email>
api.add_resource(VistaTokenacceso, '/tokenacceso')
api.add_resource(Test, '/ping')
jwt = JWTManager(application)

if __name__ == "__main__":
    application.run(port = 5000, debug = True)

###PRUEBA PARA LA INSERTCION
##with app.app_context():
##  blacklists_schema = BlacklistsSchema()
##    c = Blacklists(email='marinasan5507@hotmail.com', app_uuid=App_uuid.MOVIL, blocked_reason='Prueba e integracion')
##    db.session.add(c)
##    db.session.commit()
##    print([blacklists_schema.dumps(blacklists) for blacklists in Blacklists.query.all()])
