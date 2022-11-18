from datetime import datetime

from app import db


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    nombre = db.Column(db.String(100))
    locacion = db.Column(db.String(30))
    informacion = db.Column(db.String(250))
    fecha_creacion = db.Column(db.DateTime())
    ultima_conexion = db.Column(db.DateTime(), default=datetime.utcnow())
    avatar = db.Column(db.String(300))