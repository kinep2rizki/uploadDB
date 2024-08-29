from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os   # Corrected the spelling

load_dotenv()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SUPABASE_DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

db = SQLAlchemy()

# Define the SupaUser model
class SupaUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)

# Create all tables
with app.app_context():
    db.create_all()

# Route to upload a new user to Supabase
@app.route('/upload_user', methods=['POST'])
def upload_user():
    data = request.json
    
    # Ensure that both username and email are provided
    if not data.get('username') or not data.get('email'):
        return jsonify({"error": "Please provide both username and email"}), 400

    # Check if the username already exists
    existing_user = SupaUser.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    # Create new user
    new_user = SupaUser(username=data['username'], email=data['email'])
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User added successfully!"}), 201

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)