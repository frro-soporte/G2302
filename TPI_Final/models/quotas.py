from data.db import db

class quota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calendarId = db.Column(db.Integer, db.ForeignKey('calendar_year.id'), nullable=False)
    quota = db.Column(db.Integer, nullable=False)
    createDate = db.Column(db.DateTime, nullable=False)
    finalDate = db.Column(db.DateTime)
    state = db.Column(db.Integer)

def __init__(self, userId, calendarId,quota,createDate, finalDate, state):
    
    self.userId = userId
    self.calendarId = calendarId
    self.quota = quota
    self.createDate = createDate
    self.finalDate = finalDate
    self.state = state