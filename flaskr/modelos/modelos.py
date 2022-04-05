from pyexpat import model
from xml.etree.ElementInclude import include
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import socket
import enum

db = SQLAlchemy()

class App_uuid(enum.Enum):
    MOVIL = 1 
    PC    = 2 


class Blacklists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))           ###el email del cliente a agregar a la lista negra global
    app_uuid = db.Column(db.Enum(App_uuid))            ###el id de la app cliente (es un UUID obligatorio)
    blocked_reason = db.Column(db.String(255))  ###el motivo por el que se agrega a la lista negra (campo opcional de máximo 255 caracteres)
    ip_adress = db.Column(db.String(128), nullable = False, default = socket.gethostbyname(socket.gethostname()))
    date_time = db.Column(db.DateTime, nullable = False, default = datetime.now()) 
       
    ##def __repr__(self) -> str:
    ##    return "{}-{}-{}".format(self.email, self.app_uuid, self.blocked_reason )*/


class EnumAppcliente(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'id':value.value, 'app':value.name}


class BlacklistsSchema(SQLAlchemyAutoSchema):
    app_uuid = EnumAppcliente(attribute='app_uuid') 
    class Meta:
        model = Blacklists
        include_relationships = True
        load_instance = True