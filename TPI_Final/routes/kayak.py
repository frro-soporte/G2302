import json
from flask import Blueprint, render_template, request, redirect, session, url_for, flash,jsonify, abort
from models.kayak import kayak
from models.kayaktype import kayaktype
from models.user import user
from models.hanger import hanger
from models.location import location
from data.db import db
from flask_login import current_user, login_required
from menu.menu import Menu

import uuid
import os

from io import BytesIO
from PIL import Image
import base64


kayaks = Blueprint('kayaks', __name__)

@kayaks.route("/kayak", methods=["GET"])
@login_required
def getAll():
    val = kayak.query.all()
    return render_template('kayak/list.html', datas = val,menues = Menu.MenuesStatic(current_user.roleId))

@kayaks.route("/kayaks/<id>", methods=["GET"])
def getbyid(id):
    return kayak.query.get(id)

# @kayaks.route("/kayaks/<id>", methods=["GET"])
@kayaks.route('/selectHangers/<id>', methods=['GET'])
def selectHangers(id):
    print("locationId", id)
    hangerlist = hanger.query.filter_by(locationId=id, isFree=1).all()
    data = {}
    data['hangers'] = []

    for item in hangerlist:
        data['hangers'].append({
        'id': item.id,
        'nroHanger': item.nroHanger
        })
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
    return data

@kayaks.route("/kayaks/Upload", methods=["GET"])
def Upload():
    image_data = request.json['data']
    extension = request.json['extension']

    image_data = bytes(image_data, encoding="ascii")

    image_name = str(uuid.uuid4()) + extension

    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image_directory = os.path.join(os.getcwd(), 'static', 'upload', 'image','')

    file_path = image_directory + image_name
    
    # save image to file system
    image.save(file_path)

    response = {
        "message": "Image Uploaded",
        "body": {
            "image_id": image_name,
        }
    }
    return jsonify(response)

@kayaks.route("/kayaks/create", methods=["POST", "GET"])
def create():
    if request.method == 'GET':
        typekayak = kayaktype.query.filter_by(state=1)
        partnerslist = user.query.filter_by(roleId=3)
        menulist = Menu.MenuesStatic(current_user.roleId)
        locationlist = location.query.filter_by(state=1)
        return render_template('kayak/create.html',ktype = typekayak,menues = menulist, partners=partnerslist,locations = locationlist)
    
    kayaktypeid = request.form['kayaktypeid']
    partnerid = request.form['partner']
    locationId = request.form['locationId']
    print("rrequest.form",request.form)
    # hangerid = request.form['hangerId']
    # nroHanger = request.form['nroHanger']
    nroKayak = request.form['nroKayak']
    shovelQuantity = request.form['shovelQuantity']
    crewmember = request.form['crewmember']

    # userId = current_user.id
    # description = request.form['description']
    
    # isexist = kayak.query.filter_by(name=name).first()
    # if isexist :
    #     flash("Ya existe un tipo de kayak con ese nombre","alert alert-danger")
    #     return redirect(url_for('kayaktypes.create'))

    if kayaktypeid == '':
        flash("Debe seleccionar el tipo de kayak.","alert alert-danger")
        return redirect(url_for('kayaks.create'))
    # if len(name) > 251:
    #     flash("La cantidad de caracteres en el nombre no puede ser mayor que 100.","alert alert-danger")
    # if len(description) > 251:
    #     flash("La cantidad de caracteres en la descripcion no puede ser mayor que 250.","alert alert-danger")
    #     return redirect(url_for('kayaktypes.create'))

    add = kayak(partnerid,kayaktypeid,locationId,1)

    db.session.add(add)
    db.session.commit()

    flash("El tipo de kayak se guardo correctamente", "alert alert-success")

    return redirect(url_for('kayaks.getAll'))

@kayaks.route("/kayaks/update/<id>", methods=["POST", "GET"])
def update(id):
    if request.method == 'POST':
        update = kayak.query.get(id)
        
        update.name = request.form['name']
        update.description = request.form['description']
        
        db.session.commit()

        flash("El tipo de kayak  se actualizo correctamente", "alert alert-success")

        return redirect(url_for('kayaktypes.getAll'))
    else:    
        updateid = kayak.query.get(id)
        return render_template('kayaks/kayaktype/update.html', updates=updateid,menues = Menu.MenuesStatic(current_user.roleId))

@kayaks.route("/kayaks/delete/<id>")
def delete(id):
   try:
        dele = kayak.query.get(id)
        db.session.delete(dele)
        db.session.commit()
        
        flash("kayaks se elimino correctamente", "alert alert-success")

        return redirect(url_for('kayaktypes.getAll'))
   except Exception as ex:
        flash("No se puede eliminar este tipo de kayak porque tiene kayak asociado","alert alert-danger")
        return redirect(url_for('kayaktypes.getAll'))