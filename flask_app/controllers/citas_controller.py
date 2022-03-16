from flask import render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.user import User
from flask_app.models.cita import Cita

@app.route("/new/cita")
def new_cita():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    user = User.get_by_id(data)

    return render_template('add_cita.html', user=user)

@app.route("/create/cita", methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    # formulario = {
    #     "name": request.form['name'],
    #     "description": request.form['description'],
    #     "instructions": request.form['instructions'],
    #     "data_made": request.form['data_made'],
    #     "user_id": request.form['user_id'],
    #     "under30": int(request.form['under30']),
    # }
    if not Cita.valida_cita(request.form):
        return redirect("/new/cita")
    Cita.save(request.form)
    return redirect("/dashboard")

@app.route("/edit/cita/<int:id>")
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    user = User.get_by_id(data)

    #Necesitamos los datos de la cita
    data_cita = {
        "id": id
    }
    cita = Cita.get_by_id(data_cita)

    return render_template('edit_cita.html', user=user, cita=cita)

@app.route("/update/cita", methods=["POST"])
def update_cita():
    if 'user_id' not in session:
        return redirect('/')

    if not Cita.valida_cita(request.form):
        return redirect("/edit/cita/"+request.form['id'])
    
    Cita.update(request.form)

    return redirect("/dashboard")

@app.route("/delete/cita/<int:id>")
def delete_cita(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id":id
    }

    Cita.delete(data)
    return redirect("/dashboard")