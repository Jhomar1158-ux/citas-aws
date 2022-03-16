from flask import render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.user import User
from flask_app.models.cita import Cita

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=['POST'])
def register():
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password'])

    formulario = {
        "first_name": request.form['first_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario)

    session['user_id'] = id

    return redirect('/dashboard')

@app.route("/login", methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    #user = User -> first_name, last_name, password, email ....

    if not user:
        flash("E-mail no encontrado", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrecto", "login")
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }
    
    user = User.get_by_id(data)
    #Citas
    citas = Cita.get_all(data)


    # Citas Pasadas 
    past_citas=Cita.citas_pasadas(data)

    # En caso no tengas citas
    if not citas:
        return render_template('citas.html', user=user, citas=citas, past_citas=past_citas)
    
    return render_template('citas.html', user=user, citas=citas, past_citas=past_citas)


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')