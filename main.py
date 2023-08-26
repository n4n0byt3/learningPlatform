from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import secrets
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db'
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)  # For generating secure tokens
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'shiv.chop0301@gmail.com'
app.config['MAIL_PASSWORD'] = 'N4N0-_-BYT3'
db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20))
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(120))  # Add this field for verification token

@app.route('/api/register', methods=['POST'])
def register_new_user():
    data = request.json
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    phone_number = data.get('phone_number')

    # Basic validation
    if not (username and email and password and confirm_password):
        return jsonify({'error': 'All fields are required'}), 400
    
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password, method='sha256')
    
    # ... Save other user data and generate verification token ...

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        phone_number=phone_number,
        # verification_token=verification_token
    )
    db.session.add(new_user)
    db.session.commit()

    # Send verification email and return response

if __name__ == '__main__':
    app.run()