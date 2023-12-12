from data.db import db

class tariff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(250))
    createDate = db.Column(db.DateTime, nullable=False)
    finalDate = db.Column(db.DateTime)
    state = db.Column(db.Integer)

def __init__(self, userId, amount, name, description,createDate, finalDate, state):
    
    self.userId = userId
    self.amount = amount
    self.name = name
    self.description = description
    self.createDate = createDate
    self.finalDate = finalDate
    self.state = state