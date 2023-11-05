from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    column1 = db.Column(db.String(255))
    column2 = db.Column(db.String(255))
    
    def __init__(self, column1, column2):
        self.column1 = column1
        self.column2= column2
