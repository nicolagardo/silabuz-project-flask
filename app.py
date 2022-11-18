from datetime import datetime
import os, hashlib
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from forms import PostForm
from models.permissions import Permission
from models.posts import Posts

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route("/", methods=['GET', 'POST'])
#login_required
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Posts(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    posts = Posts.query.order_by(Posts.time_stamp.desc()).all()
    return render_template('posts.html', **form, posts=posts, WRITE = Permission.WRITE)

@app.route('/landing')
def landing():
    if current_user.is_authenticated:
        return render_template("landing.html", status=current_user.is_authenticated)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    import models.users
    if request.method == "POST":
        from models.users import Users

        correoE = request.form.get("correoR")
        contrasenaE = request.form.get("contrasenaR")

        if request.form.get(("rememberR")):
            rememberE = True
        else:
            rememberE = False
        user = Users.query.filter_by(correo=correoE).first()

        if user is None:
            flash("Correo invalido o contrasena")
            return redirect(url_for('login'))
        elif user.check_password(contrasenaE):
            login_user(user, remember=rememberE)
            return redirect(url_for('landing'))
        else:
            flash("Correo invalido o contrasena")
            return redirect(url_for('login'))

    return render_template("index.html")


@app.route('/logout')
def logout():
        
        from models.profiles import Profile

        updatedprofile = Profile.query.filter_by(user_id=current_user.id).first()
        updatedprofile.ultima_conexion = datetime.utcnow()


        db.session.add(updatedprofile)
        db.session.commit()



        logout_user()
        return render_template("index.html")

@app.route('/registro', methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuarioE = request.form.get("usuarioR")
        emailE = request.form.get("correoR")
        passwordE = request.form.get("passR")

        from models.users import Users
        newuser = Users(usuario=usuarioE, correo=emailE)
        newuser.set_password(passwordE)

        db.session.add(newuser)
        db.session.commit()

        nombreE = request.form.get("nombreR")
        locacionE = request.form.get("locacionR")
        informacionE = request.form.get("informacionR")
        fecha_creacionE = datetime.utcnow()
        avatarE = newuser.gravatar(emailE, ratingE="pg") 

        user = Users.query.filter_by(correo=newuser.correo).first()
        from models.profiles import Profile
        newprofile = Profile(user_id=user.id, nombre=nombreE, locacion=locacionE, informacion=informacionE, fecha_creacion=fecha_creacionE, avatar=avatarE)


        db.session.add(newprofile)
        db.session.commit()


    return render_template("registro.html")


@app.route("/usuario")
@login_required
def usuario():
    from models.users import Users
    from models.profiles import Profile

    correo = current_user.correo
    userE = Users.query.filter_by(correo=correo).first_or_404()
    profileE = Profile.query.filter_by(user_id=userE.id).first_or_404()
    return render_template("usuario.html", user=userE, profile=profileE)


@app.route("/editarusuario", methods=["GET", "POST"])
def editarusuario():
    from models.users import Users
    from models.profiles import Profile

    correo = current_user.correo
    userE = Users.query.filter_by(correo=correo).first_or_404()
    profileE = Profile.query.filter_by(user_id=userE.id).first_or_404()

    if request.method == "POST":
        profileupdate = Profile.query.filter_by(user_id=current_user.id).first()

        nombreE = request.form.get("nombreR")
        locacionE = request.form.get("locacionR")
        informacionE = request.form.get("informacionR")

        profileupdate.nombre = nombreE
        profileupdate.locacion = locacionE
        profileupdate.informacion = informacionE

        db.session.commit()




        correo = current_user.correo
        userE = Users.query.filter_by(correo=correo).first_or_404()
        profileE = Profile.query.filter_by(user_id=userE.id).first_or_404()

        return redirect(url_for("usuario"))



    return render_template("editarperfil.html", perfil=profileE)


@app.route('/actualizar', methods=["GET", "POST"])
@login_required
def actualizar():
    from models.users import Users
    lsUsers = Users.query.all()

    if request.method == "POST":
        oldemail = request.form.get("oldcorreoR")
        email = request.form.get("correoR")

        from models.users import Users
        user = Users.query.filter_by(correo=oldemail).first()

        user.correo = email
        db.session.commit()

    return render_template("actualizar.html", users=lsUsers)


@app.route('/eliminar', methods=["GET", "POST"])
@login_required
def eliminar():
    from models.users import Users
    lsUsers = Users.query.all()

    if request.method == "POST":
        email = request.form.get("correoR")

        from models.users import Users
        user = Users.query.filter_by(correo=email).first()

        db.session.delete(user)
        db.session.commit()

    return render_template("eliminar.html", users=lsUsers)


# def gravatar(email, sizeE=256, defaultE="identicon", ratingE="g"):
#     urlE = 'https://secure.gravatar.com/avatar'
#     hashE = hashlib.md5(email.encode('utf-8')).hexdigest()
#     return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=urlE, hash=hashE, size=sizeE, default=defaultE, rating=ratingE)

if __name__ == '__main__':
    app.run()
