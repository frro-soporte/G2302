from data.db import db

class payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    kayakId = db.Column(db.Integer, db.ForeignKey('kayak.id'), nullable=False)
    paymentTypeId = db.Column(db.Integer, db.ForeignKey('payment_type.id'), nullable=False)
    quotaId = db.Column(db.Integer, db.ForeignKey('quota.id'), nullable=False)
    tariffId = db.Column(db.Integer, db.ForeignKey('tariff.id'), nullable=False)
    description = db.Column(db.String(250))
    createDate = db.Column(db.DateTime, nullable=False)
    finalDate = db.Column(db.DateTime)
    state = db.Column(db.Integer)

def __init__(self, userId, kayakId, quotaId, tariffId, paymentTypeId, description,createDate, finalDate, state):
    
    self.userId = userId
    self.kayakId = kayakId
    self.paymentTypeId = paymentTypeId
    self.quotaId = quotaId
    self.tariffId = tariffId
    self.description = description
    self.createDate = createDate
    self.finalDate = finalDate
    self.state = state