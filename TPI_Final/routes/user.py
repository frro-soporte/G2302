
from flask import Blueprint, render_template, request, redirect, url_for, flash
from menu.menu import Menu
from models.user import user
from models.role import role
from data.db import db
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash


users = Blueprint('users', __name__)

@users.route("/user", methods=["GET"])
def getAll():
    # usr = user.query.all()
    userfilter = user.query.all()
    return render_template('user/list.html',userfilter = userfilter,menues = Menu.MenuesStatic(current_user.roleId))

    # return render_template('role/list.html',roles=roles)

@users.route("/user/<id>", methods=["GET"])
def getbyid(id):
    return "Role by id"

@users.route("/user/create", methods=["POST", "GET"])
#@login_required
def create():
    roles = role.query.all()

    if current_user.is_authenticated:
        menulist = Menu.MenuesStatic(current_user.roleId)
    else:
        menulist = []

    #menulist = Menu.MenuesStatic(current_user.roleId)
    if request.method == 'GET':
        return render_template('user/create.html',roles=roles,menues = menulist)
    
    roleId = request.form['roleId']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    address = request.form['address']
    phone = request.form['phone']
    docNumber = request.form['docNumber']
    mail = request.form['mail']
    userName = request.form['userName']
    userPass = request.form['userPass']

    isExistUser = user.query.filter_by(userName=userName).first()
    if  isExistUser:
        flash("Existe un usuario con ese nombre","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist)
    if roleId == '':
        flash("Debe seleccionar el permiso","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist)
    if firstName == '':
        flash("Debe ingresar el nombre","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist)
    if lastName == '':
        flash("Debe ingresar el apellido","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist)
    if address == '':
        flash("Debe ingresar la direccion","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist)
    if phone == '':
        flash("Debe ingresar el telefono","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist)
    if docNumber == '':
        flash("Debe ingresar el numero de documento","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist)
    if mail == '':
        flash("Debe ingresar el correo electronico","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist)
    if userName == '':
        flash("Debe ingresar el nombre de usuario","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist) 
    if userPass == '':
        flash("Debe ingresar la contraseña del usuario","alert alert-danger")
        return render_template('user/create.html',roles=roles,menues = menulist)      

    new_user = user(roleId,firstName,lastName,address,phone,docNumber,mail,userName,userPass,1)

    db.session.add(new_user)
    db.session.commit()

    flash("El usuario se guardo correctamente", "alert alert-success")

    return redirect(url_for('users.getAll'))

@users.route("/user/update/<id>", methods=["POST", "GET"])
def update(id):
    if request.method == 'POST':
        upd = user.query.get(id)

        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address = request.form['address']
        phone = request.form['phone']
        docNumber = request.form['docNumber']
        mail = request.form['mail']
        

        if firstName == '':
            flash("Debe ingresar el nombre","alert alert-danger")
            return redirect(url_for('user.create'))
        if lastName == '':
            flash("Debe ingresar el apellido","alert alert-danger")
            return redirect(url_for('user.create'))
        if address == '':
            flash("Debe ingresar la direccion","alert alert-danger")
            return redirect(url_for('user.create'))
        if phone == '':
            flash("Debe ingresar el telefono","alert alert-danger")
            return redirect(url_for('user.create'))
        if docNumber == '':
            flash("Debe ingresar el numero de documento","alert alert-danger")
            return redirect(url_for('user.create'))
        if mail == '':
            flash("Debe ingresar el correo electronico","alert alert-danger")
            return redirect(url_for('user.create')) 

        upd.firstName = firstName
        upd.lastName = lastName
        upd.address = address
        upd.phone = phone
        upd.docNumber = docNumber
        upd.mail = mail
        
        db.session.commit()

        flash("El usuario se actualizo correctamente", "alert alert-success")

        return redirect(url_for('users.getAll'))
    else:    
        updaterol = user.query.get(id)
        return render_template('user/update.html', updates=updaterol,menues = Menu.MenuesStatic(current_user.roleId))

@users.route("/user/delete/<id>")
def delete(id):
    dele = user.query.get(id)
    if dele is None:
        flash("Debe ingresar el correo electronico","alert alert-danger")

    dele.state = 2    
    db.session.commit()
    
    flash("El permiso se elimino correctamente", "alert alert-success")

    return redirect(url_for('users.getAll'))


@users.route("/user/reset_pass", methods=["POST", "GET"])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        user_instance = user.query.filter_by(mail=email, userName=username).first()

        if user_instance is None:
            flash("Usuario no encontrado. Verifica tu correo electrónico y nombre de usuario.", "alert alert-danger")
            return render_template('user/reset_pass.html')

        if new_password != confirm_password:
            flash("Las contraseñas no coinciden. Inténtalo de nuevo.", "alert alert-danger")
            return render_template('user/reset_pass.html')

        print(f"Email: {email}, Username: {username}, New Password: {new_password}, Confirm Password: {confirm_password}")
        print(f"User instance: {user_instance}")


        user_instance.userPass = generate_password_hash(new_password)
        db.session.commit()

        flash("Contraseña actualizada correctamente.", "alert alert-success")

        return redirect(url_for('auth.login'))

    return render_template('user/reset_pass.html')