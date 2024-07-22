#!/usr/bin/env python3
from flask import Flask, request, make_response, abort, session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from config import app, db, api
from werkzeug.exceptions import NotFound, Unauthorized
from models import User, Journal, Year, Month, Day, Task
from sqlalchemy.exc import IntegrityError
@app.route('/')
def index():
    return '<h1>MindTime</h1>'

class Users(Resource):
    def post(self):
        req_json = request.get_json()
        username = req_json['username']
        password_hash = req_json['password']

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return make_response({'error': 'Username already exists'}, 400)

        new_user = User(
            username=username,
            password_hash=password_hash
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return make_response({'error': 'An error occurred while creating the user'}, 500)

        session['user_id'] = new_user.id
        return make_response(new_user.to_dict(), 201)
@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter(User.username == request.get_json()['username']).first()
    if user and user.authenticate(request.get_json()['password']):
        session['user_id'] = user.id
        return make_response(user.to_dict(), 200)
    else:
        raise Unauthorized
    
@app.route('/logout', methods=['DELETE'])
def logout():
    session.clear()
    return make_response({}, 204)

class Journals(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized'}, 401)
        journals = Journal.query.filter_by(user_id=user_id).all()
        return make_response([journal.to_dict() for journal in journals], 200)

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized'}, 401)
        req_json = request.get_json()
        new_journal = Journal(
            content=req_json['content'],
            day_id=req_json['day_id'],
            user_id=user_id
        )
        db.session.add(new_journal)
        db.session.commit()
        return make_response(new_journal.to_dict(), 201)

class Journalsbyid(Resource):
    def patch(self, journal_id):
        journal = Journal.query.get(journal_id)
        if not journal:
            return make_response({'error': 'Journal not found'}, 404)
        req_json = request.get_json()
        for key, value in req_json.items():
            setattr(journal, key, value)
        db.session.add(journal)
        db.session.commit()
        return make_response(journal.to_dict(), 200)

    def delete(self, journal_id):
        journal = Journal.query.get(journal_id)
        if not journal:
            return make_response({'error': 'Journal not found'}, 404)
        db.session.delete(journal)
        db.session.commit()
        return make_response({}, 204)

    def get(self, journal_id):
        journal = Journal.query.filter_by(id=journal_id).first()
        if journal is None:
            return make_response({'error': 'Journal not found'}, 404)
        return make_response(journal.to_dict(), 200)

class Tasks(Resource):
    def get(self):
        tasks = Task.query.all()
        return make_response([task.to_dict() for task in tasks], 200)

    def post(self):
        req_json = request.get_json()
        new_task = Task(
            description=req_json['description'],
            day_id=req_json['day_id'],
            completed=req_json.get('completed', False)
        )
        db.session.add(new_task)
        db.session.commit()
        return make_response(new_task.to_dict(), 201)

class Tasksbyid(Resource):
    def patch(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return make_response({'error': 'Task not found'}, 404)
        req_json = request.get_json()
        for key, value in req_json.items():
            setattr(task, key, value)
        db.session.add(task)
        db.session.commit()
        return make_response(task.to_dict(), 200)

    def delete(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return make_response({'error': 'Task not found'}, 404)
        db.session.delete(task)
        db.session.commit()
        return make_response({}, 204)

    def get(self, task_id):
        task = Task.query.filter_by(id=task_id).first()
        if task is None:
            return make_response({'error': 'Task not found'}, 404)
        return make_response(task.to_dict(), 200)

class Years(Resource):
    def get(self):
        years = [year.to_dict() for year in Year.query.all()]
        return make_response(years, 200)

    def post(self):
        req_json = request.get_json()
        new_year = Year(year=req_json['year'])
        db.session.add(new_year)
        db.session.commit()
        return make_response(new_year.to_dict(), 201)

class Yearsbyid(Resource):
    def patch(self, year_id):
        year = Year.query.get(year_id)
        if not year:
            return make_response({'error': 'Year not found'}, 404)
        req_json = request.get_json()
        for key, value in req_json.items():
            setattr(year, key, value)
        db.session.add(year)
        db.session.commit()
        return make_response(year.to_dict(), 200)

    def delete(self, year_id):
        year = Year.query.get(year_id)
        if not year:
            return make_response({'error': 'Year not found'}, 404)
        db.session.delete(year)
        db.session.commit()
        return make_response({}, 204)
    
    def get(self, year_id):
        year = Year.query.filter_by(id=year_id).first()
        if year is None:
            return make_response({'error': 'Year not found'}, 404)
        return make_response(year.to_dict(), 200)

class Months(Resource):
    def get(self):
        months = [month.to_dict() for month in Month.query.all()]
        return make_response(months, 200)

    def post(self):
        req_json = request.get_json()
        new_month = Month(
            month=req_json['month'],
            year_id=req_json['year_id']
        )
        db.session.add(new_month)
        db.session.commit()
        return make_response(new_month.to_dict(), 201)

class Monthsbyid(Resource):
    def patch(self, month_id):
        month = Month.query.get(month_id)
        if not month:
            return make_response({'error': 'Month not found'}, 404)
        req_json = request.get_json()
        for key, value in req_json.items():
            setattr(month, key, value)
        db.session.add(month)
        db.session.commit()
        return make_response(month.to_dict(), 200)

    def delete(self, month_id):
        month = Month.query.get(month_id)
        if not month:
            return make_response({'error': 'Month not found'}, 404)
        db.session.delete(month)
        db.session.commit()
        return make_response({}, 204)
    
    def get(self, month_id):
        month = Month.query.filter_by(id=month_id).first()
        if month is None:
            return make_response({'error': 'Month not found'}, 404)
        return make_response(month.to_dict(), 200)

class Days(Resource):
    def get(self):
        days = [day.to_dict() for day in Day.query.all()]
        return make_response(days, 200)

    def post(self):
        req_json = request.get_json()
        new_day = Day(
            day=req_json['day'],
            month_id=req_json['month_id']
        )
        db.session.add(new_day)
        db.session.commit()
        return make_response(new_day.to_dict(), 201)

class Daysbyid(Resource):
    def patch(self, day_id):
        day = Day.query.get(day_id)
        if not day:
            return make_response({'error': 'Day not found'}, 404)
        req_json = request.get_json()
        for key, value in req_json.items():
            setattr(day, key, value)
        db.session.add(day)
        db.session.commit()
        return make_response(day.to_dict(), 200)

    def delete(self, day_id):
        day = Day.query.get(day_id)
        if not day:
            return make_response({'error': 'Day not found'}, 404)
        db.session.delete(day)
        db.session.commit()
        return make_response({}, 204)
    
    def get(self, day_id):
        day = Day.query.filter_by(id=day_id).first()
        if day is None:
            return make_response({'error': 'Day not found'}, 404)
        return make_response(day.to_dict(), 200)

# Add resources to the API
api.add_resource(Users, '/users', '/signup')
api.add_resource(Journals, '/journals')
api.add_resource(Tasks, '/tasks')
api.add_resource(Years, '/years')
api.add_resource(Months, '/months')
api.add_resource(Days, '/days')
api.add_resource(Journalsbyid,'/journals/<int:journal_id>')
api.add_resource(Tasksbyid,'/tasks/<int:task_id>')
api.add_resource(Yearsbyid,'/years/<int:year_id>')
api.add_resource(Monthsbyid,'/months/<int:month_id>')
api.add_resource(Daysbyid,'/days/<int:day_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
