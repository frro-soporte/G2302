from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import user
from data.db import db
from flask_login import current_user, login_required
from menu.menu import Menu


reports = Blueprint('reports', __name__)

@reports.route("/report/month", methods=["GET"])
@login_required
def getAll():
    return render_template('report/month.html')