from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.hanger import hanger
from models.location import location
from data.db import db
from flask_login import current_user, login_required,current_user
from menu.menu import Menu;
from datetime import datetime


hangers = Blueprint('hangers', __name__)

@hangers.route("/hangers", methods=["GET"])
@login_required
def getAll():
    hangs = hanger.query.filter_by(state=1)
    loc = location.query.filter_by(state=1)  
    return render_template('hanger/list.html', hang = hangs, loc = loc,menues = Menu.MenuesStatic(current_user.roleId))

@hangers.route("/hanger/create", methods=["POST", "GET"])
@login_required
def create():
    if request.method == 'GET':
        loc = location.query.all()
        return render_template('hanger/create.html', loc = loc,menues = Menu.MenuesStatic(current_user.roleId))
    
    nroHanger = request.form['nroHanger']
    description = request.form['description']
    idLocation = request.form['location']
    createDate = datetime.now()
    userId = current_user.id
    finalDate = None
    state = 1
    isexist = hanger.query.filter_by(nroHanger=nroHanger,locationId=idLocation,state=1).first()
    if isexist :
        flash("Ya existe un perchas con ese numero para esa zona","alert alert-danger")
        return redirect(url_for('hangers.create'))
    if nroHanger == '':
        flash("Debe ingresar el número de hanger","alert alert-danger")
        return redirect(url_for('hangers.create'))
    
    add = hanger(nroHanger=nroHanger, locationId = idLocation, userId=userId, description=description, createDate = createDate,finalDate=finalDate, state=state)
    db.session.add(add)
    db.session.commit()

    flash("El hanger se guardo correctamente", "alert alert-success")

    return redirect(url_for('hangers.getAll'))

@hangers.route("/hanger/update/<id>", methods=["POST", "GET"])
@login_required
def update(id):
    if request.method == 'POST':
        h = hanger.query.get(id)
        h.nroHanger = request.form['nroHanger']
        h.locationId = request.form['location']
        h.description = request.form['description']
        db.session.commit()

        flash("El hanger se actualizo correctamente", "alert alert-success")

        return redirect(url_for('hangers.getAll'))
    else:    
        updateid = hanger.query.get(id)
        loc = location.query.all()
        return render_template('hanger/update.html', hanger=updateid, loc = loc,menues = Menu.MenuesStatic(current_user.roleId))


@hangers.route("/hanger/delete/<id>")
@login_required
def delete(id):
   try:
        h = hanger.query.get(id)
        h.finalDate = datetime.now()
        h.state = 0
        db.session.commit()
        
        flash("El hanger se eliminó correctamente", "alert alert-success")

        return redirect(url_for('hangers.getAll'))
   except Exception as ex:
        flash("No se puede eliminar este hanger","alert alert-danger")
        return redirect(url_for('hangers.getAll'))
   