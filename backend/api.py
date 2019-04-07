from flask import Blueprint, jsonify, request
from random import *
from flask_cors import CORS
from flask import make_response

from backend import app, db
from backend.models import Task

api = Blueprint('api', __name__)

@api.route('/hello/<string:name>/')
def say_hello(name):
    response = { 'msg': "Hello {}".format(name) }
    return jsonify(response)

@api.route('/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@api.route('/get', methods=['GET'])
def get_taks():
    taks = Task.query.order_by(Task.id.desc()).all()
    taks_dict = [task.to_dict() for task in taks]
    return jsonify(taks_dict)

@api.route('/add', methods=['POST'])
def add_task():
    task = Task(
        title=request.form['title'],
        text=request.form['text']
        )
    db.session.add(task)
    db.session.commit()
    task = Task.query.order_by(Task.id.desc()).first()
    id = str(task.id)
    r = make_response(id)
    return r

@api.route('/delete', methods=['POST'])
def delete_task():
    id = request.form['id']
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    r = make_response(id)
    return r

@api.route('/update', methods=['POST'])
def update_task():
    id = request.form['id']
    task = db.session.query(Task).filter(Task.id==id).first()
    task.title = request.form['title']
    task.text = request.form['text']
    db.session.commit()
    r = make_response(id)
    return r