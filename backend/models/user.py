from db import db
from hashlib import sha256

class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema':'emaildatabase'}
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(40))
    password = db.Column(db.String(50))

    def hash_password(passkey):
        return sha256(passkey.encode()).hexdigest()

    @classmethod
    def get_user_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.delete()