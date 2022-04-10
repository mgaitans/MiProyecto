from flask_restful import Resource
from modelos import db, Blacklists, BlacklistsSchema
from flask import request
from flask_jwt_extended import jwt_required, create_access_token


blacklists_schema = BlacklistsSchema()

class VistaTokenacceso(Resource):
    def post(self):
        token_de_acceso = create_access_token(identity=request.json['usuario'])
        return {'mensaje':'token de acceso creado de manera exitosa', 'token de acceso':token_de_acceso}

class VistaBlacklists(Resource):
    
    @jwt_required()
    def get(self):
        return [blacklists_schema.dump(blacklists) for blacklists in Blacklists.query.all()]

    @jwt_required()
    def post(self):
        email_exist = Blacklists.query.filter(Blacklists.email == request.json["email"]).all()
        if len(email_exist) > 0:
            return{"mensaje":"El email a ingresar en la lista negra ya existe. No se puede registrar de nuevo.","datos":0}, 400
        else:
            add_blacklist = Blacklists(email=request.json['email'], app_uuid=request.json['app_uuid'], blocked_reason=request.json['blocked_reason'])
            db.session.add(add_blacklist)
            db.session.commit()
            return {"mensaje":"email se agrego a la lista negra de manera exitosa.", "datos":blacklists_schema.dump(add_blacklist)}, 200
            ##return blacklists_schema.dump(add_blacklist)

class VistaBlacklist(Resource):
    
    @jwt_required()
    def get(self, email):
        email_exist = Blacklists.query.filter(Blacklists.email == email).all()
        if len(email_exist) > 0:
            blacklist =  Blacklists.query.filter(Blacklists.email == email).first()
            return{"mensaje":"email " + email + " existente en la lista negra. ", "datos":0 }, 200
        else:
            return{"mensaje":"email " + email + " no existente en la lista negra. ","datos":0}, 400


class Test(Resource):
    def get(self):
        return{"mensaje":"Auuuuuuuuu" }, 200
       