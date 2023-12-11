from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.tariff import tariff
from data.db import db
from flask_login import current_user, login_required
from menu.menu import Menu


tariffs = Blueprint('tariff', __name__)

@tariffs.route("/tariff", methods=["GET"])
@login_required
def getAll():
    tarifas = tariff.query.all()
    return render_template('tariff/list.html', tar=tarifas)


@tariffs.route('/tariff/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('tariff/create.html')
    
    if request.method == 'POST':

        name = request.form['name']
        amount = request.form['amount']
        description = request.form['description']
        createDate = datetime.now()
        userId = current_user.id
        finalDate = None
        state = 1


        if name == '':
            flash("Debe ingresar el nombre","alert alert-danger")
            return redirect(url_for('tariff.create'))
        
        if amount == '':
            flash("Debe ingresar la cantidad","alert alert-danger")
            return redirect(url_for('tariff.create'))
        
        if description == '':
            flash("Debe ingresar la descripción","alert alert-danger")
            return redirect(url_for('tariff.create'))
        
        add = tariff(userId=userId, name=name, amount=amount, description=description, createDate=createDate, finalDate=finalDate, state=state)
        db.session.add(add)
        db.session.commit()

        flash("La tarifa se creó correctamente", "alert alert-success")

        return redirect(url_for('tariff.getAll'))
    


@tariffs.route('/tariff/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        update = tariff.query.get(id)
        update.name = request.form['name']
        update.amount = request.form['amount']
        update.description = request.form['description']
        
        db.session.commit()

        flash("La tarifa se actualizó correctamente", "alert alert-success")

        return redirect(url_for('tariff.getAll'))
    else:    
        updateid = tariff.query.get(id)
        return render_template('tariff/update.html', t=updateid)



@tariffs.route("/tariff/delete/<id>")
@login_required
def delete(id):
   try:
        dele = tariff.query.get(id)
        dele.finalDate = datetime.now()
        dele.state = 0
        db.session.commit()
        
        flash("La tarifa se eliminó correctamente", "alert alert-success")

        return redirect(url_for('tariff.getAll'))
   except Exception as ex:
        flash("No se puede eliminar la tarifa porque tiene una entidad asociada","alert alert-danger")
        return redirect(url_for('tariff.getAll'))