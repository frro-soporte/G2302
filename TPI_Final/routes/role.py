from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.role import role
from data.db import db
from flask_login import login_required

roles = Blueprint('roles', __name__)

@roles.route("/role", methods=["GET"])
@login_required
def getAll():
    print("getAll")
    roles = role.query.all()
    return render_template('role/list.html',roles=roles)

@roles.route("/roles/<id>", methods=["GET"])
def getbyid(id):
    return "Role by id"

@roles.route("/create", methods=["POST", "GET"])
def create():
    if request.method == 'GET':
        return render_template('role/create.html')
    
    name = request.form['name']
    
    createrol = role.query.filter_by(name=name).first()
    if createrol :
        flash("Ya existe un permiso con ese nombre","alert alert-danger")
        return redirect(url_for('roles.create'))

    if name == '':
        flash("Debe ingresar el nombre","alert alert-danger")
        return redirect(url_for('roles.create'))
    
    description = request.form['description']

    new_role = role(name,description,1)

    db.session.add(new_role)
    db.session.commit()

    flash("El permiso se guardo correctamente", "alert alert-success")

    return redirect(url_for('roles.getAll'))

@roles.route("/update/<id>", methods=["POST", "GET"])
def update(id):
    if request.method == 'POST':
        updaterol = role.query.get(id)

        updaterol.name = request.form['name']
        updaterol.description = request.form['description']
        
        db.session.commit()

        flash("El permiso se actualizo correctamente", "alert alert-success")

        return redirect(url_for('roles.getAll'))
    else:    
        updaterol = role.query.get(id)
        return render_template('role/update.html', updates=updaterol)

@roles.route("/delete/<id>")
def delete(id):
   try:
        delrol = role.query.get(id)
        db.session.delete(delrol)
        db.session.commit()
        
        flash("El permiso se elimino correctamente", "alert alert-success")

        return redirect(url_for('roles.getAll'))
   except Exception as ex:
        flash("No se puede eliminar este permiso porque tiene un usuario asociado a este permiso","alert alert-danger")
        return redirect(url_for('roles.getAll'))