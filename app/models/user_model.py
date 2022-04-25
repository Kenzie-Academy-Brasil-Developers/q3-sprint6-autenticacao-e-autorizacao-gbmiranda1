from werkzeug.security import generate_password_hash, check_password_hash
from app.configs.database import db
from dataclasses import dataclass

@dataclass
class UserModel(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    last_name = db.Column(db.String(511), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(511), nullable=False)

    @property
    def password(self):
        raise AttributeError('password cannot be accessed')
    
    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)
        
    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash,password_to_compare)