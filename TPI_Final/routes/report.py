from data.db import db
from datetime import datetime

class Rental(db.Model):
    __tablename__ = 'rental'

    id = db.Column(db.Integer, primary_key=True)
    kayak_id = db.Column(db.Integer, db.ForeignKey('kayak.id'), nullable=False)
    rental_date = db.Column(db.Date, default=datetime.now().date(), nullable=False)
    rental_time = db.Column(db.Time, default=datetime.now().time(), nullable=False)

    def __init__(self, kayak_id, rental_date=None, rental_time=None):
        self.kayak_id = kayak_id
        self.rental_date = rental_date or datetime.now().date()
        self.rental_time = rental_time or datetime.now().time()