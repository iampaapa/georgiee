from .extensions import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    dob = db.Column(db.String(75))
    gender = db.Column(db.String(50))
    number = db.Column(db.String(50))
    classOfUser = db.Column(db.String(75))
