from email import header
from email.mime import application
import unittest
from modelos.modelos import *
from application import application
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Test_Pruebas(unittest.TestCase):

    def setUp(self):
        application.config['TESTING'] = True
        application.config['DEBUG'] = True
        application.config['APP_ENV'] = 'APP_ENV_TESTING'
        application.config['WTF_CSRF_ENABLED'] = False
        self.client = application.test_client()
        db.drop_all()
        db.create_all()
        

    def test_consulta(self):
        token =  rec = self.client.post('/tokenacceso',json={'usuario': 'admin'})
        tokenStr = token.get_json()
        tokenStr = tokenStr['token de acceso']
        rec = self.client.get('/blacklists', headers={'Authorization':"Bearer "+tokenStr})
        response = rec.get_json()
        self.assertEqual(len(response), 0)

    def test_consulta_sincomentarios(self):
        token =  self.client.post('/tokenacceso',json={'usuario': 'admin'})
        tokenStr = token.get_json()
        tokenStr = tokenStr['token de acceso']

        body = {
                    "email": "magasa160@hotmail.com",
                    "app_uuid": "MOVIL",
                    "blocked_reason": "Prueba de integracion"
                }
        rec = self.client.post('/blacklists',json=body, headers={'Authorization':"Bearer "+tokenStr})
        consulta = self.client.get('/blacklists', headers={'Authorization':"Bearer "+tokenStr})
        self.assertEqual(len(consulta.get_json()), 1)
    

    def tearDown(self):
        with application.app_context():
            db.session.remove()
            