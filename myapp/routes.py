from flask import Blueprint, redirect, request, url_for, jsonify
from twilio.rest import Client
from .extensions import db
from .models import User, Candidate
import requests

main = Blueprint('main', __name__)

account_sid = "ACfec16894680f21d334f3d27fbb51fca0"
auth_token = "6d0e314340d27450a049ca51f332d98f"
verify_sid = "VAe579e07c7264a6755685f8006ef1b6a2"
client = Client(account_sid, auth_token)

@main.route('/')
def index():
    users = User.query.all()
    users_list_html = [
        f"<li>{user.username}, {user.dob}, {user.gender}, {user.number}, {user.classOfUser}, {user.voted}</li>" 
        for user in users
    ]
    return f"<ul>{''.join(users_list_html)}</ul>"

@main.route('/enroll_user', methods=['POST'])
def add_user():
    data = request.json

    # Check if all required fields are present
    required_fields = ['username', 'dob', 'gender', 'number', 'classOfUser']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    username = data['username']
    dob = data['dob']
    gender = data['gender']
    number = data['number']
    classOfUser = data['classOfUser']
    voted = False

    # Check if any of the required fields are empty
    if not all(data[field] for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    new_user = User(username=username, dob=dob, gender=gender, number=number, classOfUser=classOfUser, voted=voted)
    db.session.add(new_user)
    db.session.commit()

    user_add_response = {
        username: "added"
    }

    return jsonify(user_add_response), 200

@main.route('/find_user', methods=['POST'])
def find_user():
    number = request.json.get('number')

    if not number:
        return jsonify({"error": "Phone number is required"}), 400
    
    user = User.query.filter_by(number=number).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "username": user.username,
        "dob": user.dob,
        "gender": user.gender,
        "number": user.number,
        "classOfUser": user.classOfUser
    }

    return jsonify(user_data), 200

@main.route('/send_otp', methods=['POST'])
def send_otp():
    number = request.json.get('number')

    if not number:
        return jsonify({"error": "Phone number is required"}), 400

    user = User.query.filter_by(number=number).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    verification = client.verify.v2.services(verify_sid) \
      .verifications \
      .create(to=number, channel="sms")

    return jsonify({"message": "OTP has been sent"}), 200

@main.route('/confirm_otp', methods=['POST'])
def confirm_otp():
    number = request.json.get('number')
    otp = request.json.get('otp')

    if not number or not otp:
        return jsonify({"error": "Phone number and OTP are required"}), 400
    
    verification_check = client.verify.v2.services(verify_sid) \
      .verification_checks \
      .create(to=number, code=otp)

    if verification_check.status == "approved":
         user = User.query.filter_by(number=number).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
    
        user_data = {
            "username": user.username,
            "dob": user.dob,
            "gender": user.gender,
            "number": user.number,
            "classOfUser": user.classOfUser
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400

@main.route('/enroll_candidate', methods=['POST'])
def add_candidate():
    data = request.json

    # Check if all required fields are present
    required_fields = ['name', 'position']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    name = data['name']
    position = data['position']
    numberVotes = 0

    # Check if any of the required fields are empty
    if not all(data[field] for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    new_candidate = Candidate(name=name, position=position, numberVotes=numberVotes)
    db.session.add(new_candidate)
    db.session.commit()

    user_add_response = {
        name: "Candidate added"
    }

    return jsonify(user_add_response), 200

@main.route('/vote', methods=['POST'])
def vote_candidate():
    number = request.json.get('number')
    voted_for = request.json.get('votedFor')

    if not number or not voted_for:
        return jsonify({"error": "Number and votedFor fields are required"}), 400

    # Check whether the number is in the number column of the user database
    user = User.query.filter_by(number=number).first()

    if not user:
        return jsonify({"error": "Invalid user"}), 404

    if user.voted:
        return jsonify({"error": "You have already voted"}), 400

    candidate = Candidate.query.filter_by(name=voted_for).first()

    if not candidate:
        return jsonify({"error": f"Candidate '{voted_for}' not found"}), 404

    candidate.numberVotes += 1
    user.voted = True
    db.session.commit()

    return jsonify({"message": f"Vote added for {voted_for}"}), 200

@main.route('/results', methods=['GET'])
def get_results():
    results = {}

    candidates = Candidate.query.all()

    for candidate in candidates:
        role = candidate.position
        name = candidate.name
        total_votes = candidate.numberVotes

        if role not in results:
            results[role] = {}

        results[role][name] = total_votes

    return jsonify(results)


@main.route('/candidates_by_role', methods=['POST'])
def get_candidates_by_role():
    role = request.json.get('role')

    if not role:
        return jsonify({"error": "Role field is required"}), 400

    candidates = Candidate.query.filter_by(position=role).all()

    if not candidates:
        return jsonify({"message": f"No candidates found for role '{role}'"}), 404

    candidate_names = [candidate.name for candidate in candidates]

    return jsonify({role: candidate_names})
