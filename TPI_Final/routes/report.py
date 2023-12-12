from models.report import Rental
from flask import Blueprint, render_template, request, redirect, url_for, flash
from menu.menu import Menu  
from flask_login import current_user, login_required        

Rental = Blueprint('Rental', __name__)

@Rental.route("/Rental", methods=["GET"])
def getAll():
    # usr = user.query.all()
    userfilter = Rental.query.all()
    return render_template('user/list.html',userfilter = userfilter,menues = Menu.MenuesStatic(current_user.roleId))