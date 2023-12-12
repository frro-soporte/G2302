from data.db import db
from datetime import datetime

class kayak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hangerId = db.Column(db.Integer, db.ForeignKey('hanger.id'), nullable=False)
    KayaktypeId = db.Column(db.Integer, db.ForeignKey('kayaktype.id'), nullable=False)
    nroKayak = db.Column(db.String(250), nullable=False)
    shovelQuantity = db.Column(db.Integer)
    crewmember = db.Column(db.Integer)
    createDate = db.Column(db.DateTime, nullable=False)
    finalDate = db.Column(db.DateTime)
    state = db.Column(db.Integer)

    def __init__(self,userId, hangerId, KayaktypeId,nroKayak,shovelQuantity,crewmember, state = 1):
        self.userId = userId
        self.hangerId = hangerId
        self.KayaktypeId = KayaktypeId
        self.nroKayak = nroKayak
        self.shovelQuantity = shovelQuantity
        self.crewmember = crewmember
        self.createDate = datetime.now()
        self.state = state