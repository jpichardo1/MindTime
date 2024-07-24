from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import bcrypt, db
from datetime import datetime, timezone
from sqlalchemy.ext.associationproxy import association_proxy


def current_time():
    return datetime.now(timezone.utc)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    journals = db.relationship('Journal', back_populates='user', cascade='all, delete-orphan')
    tasks = association_proxy('journals', 'tasks')
    serialize_rules = ('-journals.user', '-_password_hash')

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Must have a username')
        return username

    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'

class Journal(db.Model, SerializerMixin):
    __tablename__ = "journals"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=current_time)
    updated_at = db.Column(db.DateTime, default=current_time, onupdate=current_time)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='journals')
    day = db.relationship('Day', back_populates='journals')
    tasks = association_proxy('day', 'tasks')
    
    serialize_rules = ('-user.journals', '-day.journals')

    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError('Must have content')
        return content

    def formatted_created_at(self):
        return self.created_at.strftime("%m/%d/%Y %H:%M")

    def formatted_updated_at(self):
        return self.updated_at.strftime("%m/%d/%Y %H:%M")

    def __repr__(self):
        return f'<Journal {self.id} - {self.content[:20]}>'

class Year(db.Model, SerializerMixin):
    __tablename__ = "years"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)

    months = db.relationship('Month', back_populates='year', cascade='all, delete-orphan')
    days = association_proxy('months', 'days')

    serialize_rules = ('-months.year',)

    def __repr__(self):
        return f'<Year {self.year}>'

class Month(db.Model, SerializerMixin):
    __tablename__ = "months"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year_id = db.Column(db.Integer, db.ForeignKey('years.id'), nullable=False)

    year = db.relationship('Year', back_populates='months')
    days = db.relationship('Day', back_populates='month', cascade='all, delete-orphan')

    serialize_rules = ('-year.months', '-days.month')

    def __repr__(self):
        return f'<Month {self.month} of Year {self.year.year}>'

class Day(db.Model, SerializerMixin):
    __tablename__ = "days"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month_id = db.Column(db.Integer, db.ForeignKey('months.id'), nullable=False)

    month = db.relationship('Month', back_populates='days')
    journals = db.relationship('Journal', back_populates='day', cascade='all, delete-orphan')
    tasks = db.relationship('Task', back_populates='day', cascade='all, delete-orphan')

    serialize_rules = ('-month.days', '-journals.day', '-tasks.day')

    def __repr__(self):
        return f'<Day {self.day} of Month {self.month.month} of Year {self.month.year.year}>'

class Task(db.Model, SerializerMixin):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'), nullable=False)

    day = db.relationship('Day', back_populates='tasks')

    serialize_rules = ('-day.tasks',)

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError('Must have a description')
        return description

    def __repr__(self):
        return f'<Task {self.id} - {self.description[:20]}>'