from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user,login_required,current_user

from models.role import role

from models.user import user
from models.auth import Auth
from menu.menu import Menu;
from data.db import db
import data
import json

import data
import json


auths = Blueprint('auth', __name__)

# Definir permisos
# admin_permission = Permission(RoleNeed('Admin'))
# user_permission = Permission(RoleNeed('User'))

@auths.route("/", methods=["GET"])
def login():
    return redirect('auth')

@auths.route("/auth", methods=["POST", "GET"])
def auth():
    try:
        if request.method == 'GET':
            return render_template('auth/login.html')  
    
        usrName = request.form['userName']
        userPass = request.form['userPass']
        
        if usrName == '' or userPass == '':
            flash("Debe ingresar el nombre de usuario y la contraseña", "alert alert-danger")
            return redirect(url_for('auth.login'))

        result = user.query.filter_by(userName=usrName).first()
        
        if result:
            authentication = Auth(result.id, result.roleId, result.firstName, result.lastName, result.address, result.phone, result.docNumber, result.mail, result.userName, Auth.check_password(result.userPass, userPass))
        
            if authentication.userPass:
                login_user(authentication)
                prod = json.loads(datos_JSON);  
                return render_template('layout.html',products = prod,menues = Menu.MenuesStatic(current_user.roleId)) 
            else:
                flash("Usuario y/o contraseña incorrectos", "alert alert-danger")

        else:
            flash("Usuario y/o contraseña incorrectos", "alert alert-danger")

        return render_template('auth/login.html')

    except Exception as ex:
        flash("Error en el inicio de sesión", "alert alert-danger")
        return redirect(url_for('auth.login'))

@auths.route("/home", methods=["GET"])
@login_required
def home():
    return render_template('layout.html',products =json.loads(datos_JSON),menues = Menu.MenuesStatic(current_user.roleId))
    # if admin_permission.can():
    #     return redirect(url_for('auth.login')) 
    # elif user_permission.can():
    #     return redirect(url_for('auth.login'))
# datos_diccionario = json.loads(datos_JSON)
#    print("datos_diccionario ",datos_diccionario)
#    return render_template('layout.html',products = datos_diccionario)  # Página para usuarios regulares

@auths.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def status_401(error):
    return redirect(url_for('auth.login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


datos_JSON =  """
[ {
      "name": "Quimica",
      "url": "kayak1.jpg"
    },
    {
        "name": "Administracion de recurso",
        "url": "kayak2.jpg"
    },
    {
        "name": "Economia",
        "url": "kayak3.jpg"
    },
    {
        "name": "ESTRUCTURA DE DATOS",
        "url": "kayak4.jpg"
    },
    {
        "name": "Legislation",
        "url": "CARPAS_PAGINA_WEB.jpg"
    }
]
"""