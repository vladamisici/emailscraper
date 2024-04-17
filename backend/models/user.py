from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema':'emaildatabase'}
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(40))
    password = db.Column(db.String(50))

    @staticmethod
    def hash_password(passkey):
        return generate_password_hash(passkey)
    
    @staticmethod
    def check_password(user,password):
        return check_password_hash(user.password, password)

    @classmethod
    def get_user_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.delete()