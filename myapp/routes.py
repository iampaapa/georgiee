from flask import Blueprint, redirect, request, url_for

from extensions import db
from models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    print(users)
    users_list_html = [
        f"<li>{user.username}, {user.dob}, {user.gender}, {user.number}, {user.classOfUser}</li>" 
        for user in users
    ]
    return f"<ul>{''.join(users_list_html)}</ul>"

@main.route('/add', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    dob = data.get('dob')
    gender = data.get('gender')
    number = data.get('number')
    classOfUser = data.get('classOfUser')

    new_user = User(username=username, dob=dob, gender=gender, number=number, classOfUser=classOfUser)
    db.session.add(new_user)
    db.session.commit()
    
    return "Done"
