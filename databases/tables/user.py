from databases.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    token = db.Column(db.String(500), unique = True, nullable = False)

    def __init__(self, token):
        self.token = token
