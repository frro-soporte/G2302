from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.quotas import quota
from data.db import db
from flask_login import current_user, login_required
from datetime import datetime
from models.paymentType import paymentType

paymenttype = Blueprint('paymenttype', __name__)

@paymenttype.route("/paymenttype", methods=["GET"])
@login_required
def getAll():
    payments = paymentType.query.all()
    return render_template('paymentType/list.html', payments = payments)

@paymenttype.route('/paymenttype/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('paymentType/create.html')
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        createDate = datetime.now()
        userId = current_user.id
        finalDate = None
        state = 1


        if name == '':
            flash("Debe ingresar el nombre","alert alert-danger")
            return redirect(url_for('paymenttype.create'))
        
        if description == '':
            flash("Debe ingresar la descripción","alert alert-danger")
            return redirect(url_for('paymenttype.create'))
        
        add = paymentType(userId=userId, name=name, description=description, createDate=createDate, finalDate=finalDate, state=state)
        db.session.add(add)
        db.session.commit()

        flash("El método de pago se guardó correctamente", "alert alert-success")

        return redirect(url_for('paymenttype.getAll'))
    


@paymenttype.route('/paymenttype/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        update = paymentType.query.get(id)
        
        update.name = request.form['name']
        update.description = request.form['description']
        
        db.session.commit()

        flash("El método de pago se actualizó correctamente", "alert alert-success")

        return redirect(url_for('paymenttype.getAll'))
    else:    
        updateid = paymentType.query.get(id)
        return render_template('paymentType/update.html', p=updateid)
    

@paymenttype.route("/paymenttype/delete/<id>")
@login_required
def delete(id):
   try:
        dele = paymentType.query.get(id)
        dele.finalDate = datetime.now()
        dele.state = 0
        db.session.commit()
        
        flash("El método de pago se eliminó correctamente", "alert alert-success")

        return redirect(url_for('paymenttype.getAll'))
   except Exception as ex:
        flash("No se puede eliminar este método de pago porque tiene una entidad asociada","alert alert-danger")
        return redirect(url_for('paymenttype.getAll'))