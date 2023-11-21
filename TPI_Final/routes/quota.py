from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.calendarYear import calendarYear
from models.quotas import quota
from data.db import db
from flask_login import current_user, login_required
from datetime import datetime

quotas = Blueprint('quotas', __name__)

@quotas.route("/quotas", methods=["GET"])
@login_required
def getAll():
    quotas = quota.query.all()
    calendarios =calendarYear.query.all()
    return render_template('quota/list.html',quotas = quotas, calendarios = calendarios)

@quotas.route('/quotas/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        c = calendarYear.query.all()
        return render_template('quota/create.html', calendarios=c)
    
    if request.method == 'POST':
        calendarId = request.form['calendarId']
        cuota = request.form['quota']
        createDate = datetime.now()
        userId = current_user.id
        finalDate = None
        state = 1


        if cuota == '':
            flash("Debe ingresar la cuota","alert alert-danger")
            return redirect(url_for('quotas.create'))
        
        add = quota(userId=userId, calendarId=calendarId ,quota=cuota,createDate=createDate, finalDate=finalDate, state=state)
        db.session.add(add)
        db.session.commit()

        flash("La cuota se guardó correctamente", "alert alert-success")

        return redirect(url_for('quotas.getAll'))
    


@quotas.route('/quotas/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        update = quota.query.get(id)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  ", request.form['calendarId'])
        update.calendarId = request.form['calendarId']
        update.quota = request.form['quota']
        
        db.session.commit()

        flash("La cuota se actualizó correctamente", "alert alert-success")

        return redirect(url_for('quotas.getAll'))
    else:    
        updateid = quota.query.get(id)
        calendarios = calendarYear.query.all()
        return render_template('quota/update.html', q=updateid, calendarios = calendarios)
    

@quotas.route("/quotas/delete/<id>")
@login_required
def delete(id):
   try:
        dele = quota.query.get(id)
        
        dele.finalDate = datetime.now()
        dele.state = 0
        db.session.commit()
        
        flash("La cuota se eliminó correctamente", "alert alert-success")

        return redirect(url_for('quotas.getAll'))
   except Exception as ex:
        flash("No se puede eliminar esta cuota porque tiene una entidad asociada","alert alert-danger")
        return redirect(url_for('quotas.getAll'))