#! /usr/bin/env python3
# james rogers | james.levi.rogers@gmail.com

from random import sample
import yaml
from flask import Flask, redirect, render_template, request, url_for, session
from datetime import datetime, timedelta  # <--- Added timedelta
import hashlib

# Initialize Flask application
app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)  # <--- Set session expiration

@app.route('/')
def index():
    # Retrieve stored choices from session, or use default values
    stored_ancestry = session.get('ancestry', 'Human')
    stored_gender = session.get('gender', 'male')
    stored_count = session.get('count', '5')
    return render_template('index.html',
                           ancestries=list(app.config['ancestry_generate'].keys()),
                           stored_ancestry=stored_ancestry,
                           stored_gender=stored_gender,
                           stored_count=stored_count)

@app.route('/names', methods=['POST'])
def names():
    # Retrieve user selections from form data.
    ancestry = request.form.get('ancestry', 'Human').capitalize()
    gender = request.form.get('gender', 'male').lower()
    count_str = request.form.get('count', '5')
    
    # Handle special case for ancestries with hyphens.
    if '-' in ancestry:
        parts = ancestry.split('-')
        ancestry = '-'.join([part.capitalize() for part in parts])

    # Input validations.
    if not (count_str.isdigit() and (0 < int(count_str) <= 50) and
            ancestry in app.config['ancestry_generate'] and
            gender in ['male', 'female']):
        return redirect(url_for('index'))

    # Store user's choices in the session
    session['ancestry'] = ancestry
    session['gender'] = gender
    session['count'] = count_str
    session.permanent = True  # <--- Make sure the session lifetime is respected

    # Render the names page with generated names.
    return render_template('names.html', names=generate_names_list(int(count_str), ancestry, gender))

def generate_names_list(count, ancestry, gender):
    """
    Fetch a random sample of names from the dataset based on given criteria.
    """
    return sample(app.config['ancestry_generate'][ancestry][gender], count)

if __name__ == '__main__':
    # Generate the secret key
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    secret_key = hashlib.sha256(current_time.encode()).hexdigest()
    app.config['SECRET_KEY'] = secret_key

    # Load dataset and start Flask application.
    with open('racegendernames.yaml', 'r') as yaml_file:
        app.config['ancestry_generate'] = yaml.safe_load(yaml_file)
    app.run(host='0.0.0.0', port='2224', debug=True)

