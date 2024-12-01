from ..extends import db
from sqlalchemy.orm import validates

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    phone_number = db.Column(db.String(12), unique=True)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    @validates('username', 'email', 'phone_number')
    def validate_at_least_one_field(self, key, value):
        if not value and not self.username and not self.email and not self.phone_number:
            raise ValueError('At least one field should be filled')
        return value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not (self.email or self.username or self.phone_number):
            raise ValueError('Не задано обязательного поле')
