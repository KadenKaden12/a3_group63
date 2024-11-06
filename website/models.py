from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    sur_name = db.Column(db.String(150), nullable=False)
    contact_no = db.Column(db.String(150), nullable=False)
    stress_address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.user_name}>'
    
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(300), unique=True, nullable=False)
    # events = db.relationship('Event', backref='category', lazy=True)

class Status(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(300), unique=True, nullable=False)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(300), unique=True, nullable=False)
    location = db.Column(db.String(150), unique=False, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
    start_from = db.Column(db.Time, nullable=False)
    end_to = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(300), unique=False, nullable=False)
    image_path = db.Column(db.String(500), unique=False, nullable=False)
    no_of_tickets = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    status = db.relationship('Status', backref='events')
    category = db.relationship('Category', backref='events')
    owner = db.relationship('User', backref='events')

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(300), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    no_of_tickets = db.Column(db.Integer, nullable=False)
    
    user = db.relationship('User', backref='orders')
    event = db.relationship('Event', backref='orders')
