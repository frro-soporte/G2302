from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.payment import payment
from models.paymentType import paymentType
from models.quotas import quota
from models.tariff import tariff
from models.user import user
from models.kayak import kayak
from data.db import db
from flask_login import current_user, login_required
from menu.menu import Menu



payments = Blueprint('payments', __name__)

@payments.route("/payment", methods=["GET"])
@login_required
def getAll():

    pagos = payment.query.all()
    usuarios = user.query.all()
    metodospago = paymentType.query.all()
    cuotas = quota.query.all()
    tarifas = tariff.query.all()
    return render_template('payment/list.html', pagos=pagos, usuarios = usuarios, metodospago = metodospago, cuotas = cuotas, tarifas = tarifas,menues = Menu.MenuesStatic(current_user.roleId))


@payments.route('/payment/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        usuarios = user.query.all()
        metodospago = paymentType.query.all()
        cuotas = quota.query.all()
        tarifas = tariff.query.all()
        kayaks = kayak.query.all()
        return render_template('payment/create.html', usuarios = usuarios, metodospago = metodospago, cuotas = cuotas, tarifas = tarifas, kayaks = kayaks,menues = Menu.MenuesStatic(current_user.roleId))
    
    if request.method == 'POST':
        userId = request.form['userId']
        metodopagoId = request.form['metodopago']
        cuotaId = request.form['cuota']
        tarifaId = request.form['tarifa']
        kayakId = request.form['kayak']
        description = request.form['description']
        createDate = datetime.now()
        finalDate = None
        state = 1
        
        if description == '':
            flash("Debe ingresar la descripción","alert alert-danger")
            return redirect(url_for('payments.create'))
        
        add = payment(userId=userId, kayakId=kayakId,paymentTypeId=metodopagoId, quotaId = cuotaId, tariffId=tarifaId, description=description, createDate=createDate, finalDate=finalDate, state=state)
        db.session.add(add)
        db.session.commit()

        flash("El pago se creó correctamente", "alert alert-success")

        return redirect(url_for('payments.getAll'))
    

@payments.route('/payment/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        update = payment.query.get(id)
        update.userId = request.form['userId']
        update.paymentTypeId = request.form['metodopago']
        update.quotaId = request.form['cuota']
        update.tariffId = request.form['tarifa']
        update.kayakId = request.form['kayak']
        update.description = request.form['description']
        
        db.session.commit()

        flash("El pago se actualizó correctamente", "alert alert-success")

        return redirect(url_for('payments.getAll'))
    else:    
        updateid = payment.query.get(id)
        usuarios = user.query.all()
        metodospago = paymentType.query.all()
        cuotas = quota.query.all()
        tarifas = tariff.query.all()
        kayaks = kayak.query.all()
        return render_template('payment/update.html', p=updateid,  usuarios = usuarios, metodospago = metodospago, cuotas = cuotas, tarifas = tarifas, kayaks = kayaks)
    

@payments.route("/payment/delete/<id>")
@login_required
def delete(id):
   try:
        dele = payment.query.get(id)
        dele.finalDate = datetime.now()
        dele.state = 0
        db.session.commit()
        
        flash("El pago se eliminó correctamente", "alert alert-success")

        return redirect(url_for('payments.getAll'))
   except Exception as ex:
        flash("No se puede eliminar este  pago porque tiene una entidad asociada","alert alert-danger")
        return redirect(url_for('payments.getAll'))