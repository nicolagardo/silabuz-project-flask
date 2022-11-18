from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import hashlib


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(64))
    correo = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    post = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(email, sizeE=256, defaultE="identicon", ratingE="g"):
        urlE = 'https://secure.gravatar.com/avatar'
        hashE = hashlib.md5(email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=urlE, hash=hashE, size=sizeE, default=defaultE, rating=ratingE)
