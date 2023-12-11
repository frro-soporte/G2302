from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.calendarYear import calendarYear 
from data.db import db
from flask_login import current_user, login_required
from datetime import datetime
from menu.menu import Menu

calendarYears = Blueprint('calendarYears', __name__)

@calendarYears.route("/calendarYear", methods=["GET"])
@login_required
def getAll():
    cal = calendarYear.query.all()
    return render_template('calendarYear/list.html',cal = cal,menues = Menu.MenuesStatic(current_user.roleId))

@calendarYears.route('/calendarYear/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('calendarYear/create.html',menues = Menu.MenuesStatic(current_user.roleId))
    
    if request.method == 'POST':
        yearCalendar = request.form['yearCalendar']
        description = request.form['description']
        createDate = datetime.now()
        userId = current_user.id
        finalDate = None
        state = 1


        if yearCalendar == '':
            flash("Debe ingresar el número de año","alert alert-danger")
            return redirect(url_for('calendarYears.create'))
        
        add = calendarYear(userId=userId, yearCalendar=yearCalendar ,description=description,createDate=createDate, finalDate=finalDate, state=state)
        db.session.add(add)
        db.session.commit()

        flash("El calendario se guardó correctamente", "alert alert-success")

        return redirect(url_for('calendarYears.getAll'))
    


@calendarYears.route('/calendarYear/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        update = calendarYear.query.get(id)
        
        update.yearCalendar = request.form['year']
        update.description = request.form['description']
        
        db.session.commit()

        flash("El calendario se actualizó correctamente", "alert alert-success")

        return redirect(url_for('calendarYears.getAll'))
    else:    
        updateid = calendarYear.query.get(id)
        return render_template('calendarYear/update.html', c=updateid,menues = Menu.MenuesStatic(current_user.roleId))
    

@calendarYears.route("/calendarYear/delete/<id>")
@login_required
def delete(id):
   try:
        dele = calendarYear.query.get(id)
        dele.finalDate = datetime.now()
        dele.state = 0
        db.session.commit()
        
        flash("El calendario se eliminó correctamente", "alert alert-success")

        return redirect(url_for('calendarYears.getAll'))
   except Exception as ex:
        flash("No se puede eliminar este calendario porque tiene una entidad asociada","alert alert-danger")
        return redirect(url_for('calendarYears.getAll'))