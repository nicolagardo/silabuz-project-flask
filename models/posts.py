from datetime import datetime

from ..app import db


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String(140))
    time_stamp = db.Column(db.Datetime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))