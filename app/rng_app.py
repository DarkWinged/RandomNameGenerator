#! /usr/bin/env python3

from random import sample
import yaml
from flask import Flask, redirect, render_template, request, url_for, make_response
from datetime import datetime, timedelta
import hashlib

# Initialize Flask application
app = Flask(__name__)

@app.before_request
def check_names_endpoint():
    if request.endpoint is None:
        return redirect(url_for('index'))

@app.route('/')
def index():
    # Retrieve stored choices from cookies, or use default values
    stored_ancestry = request.cookies.get('ancestry', 'Human')
    stored_gender = request.cookies.get('gender', 'male')
    stored_count = request.cookies.get('count', '5')
    stored_prefix = request.cookies.get('prefix', '')
    stored_suffix = request.cookies.get('suffix', '')
    return render_template('index.html',
                           ancestries=list(app.config['ancestry_generate'].keys()),
                           stored_ancestry=stored_ancestry,
                           stored_gender=stored_gender,
                           stored_count=stored_count,
                           stored_prefix=stored_prefix,
                           stored_suffix=stored_suffix)

@app.route('/names', methods=['POST'])
def names():
    # Retrieve user selections and prefix/suffix from form data.
    ancestry = request.form.get('ancestry', 'Human').capitalize()
    gender = request.form.get('gender', 'male').lower()
    count_str = request.form.get('count', '5')
    prefix = request.form.get('prefix', '')
    suffix = request.form.get('suffix', '')
    
    # Handle special case for ancestries with hyphens.
    if '-' in ancestry:
        parts = ancestry.split('-')
        ancestry = '-'.join([part.capitalize() for part in parts])

    # Input validations.
    if not (count_str.isdigit() and (0 < int(count_str) <= 50) and
            ancestry in app.config['ancestry_generate'] and
            gender in ['male', 'female', 'non-binary']):
        return redirect(url_for('index'))

    # Store user's choices, prefix, and suffix in cookies
    response = make_response(render_template('names.html', names=generate_names_list(int(count_str), ancestry, gender, prefix, suffix)))
    expires = datetime.now() + timedelta(days=30)  # Set the expiration time to 30 days from now
    response.set_cookie('ancestry', ancestry, expires=expires)
    response.set_cookie('gender', gender, expires=expires)
    response.set_cookie('count', count_str, expires=expires)
    response.set_cookie('prefix', prefix, expires=expires)
    response.set_cookie('suffix', suffix, expires=expires)
    return response

def generate_names_list(count, ancestry, gender, prefix, suffix):
    """
    Fetch a random sample of names from the dataset based on given criteria.
    """
    if gender == 'non-binary':
        male_names = app.config['ancestry_generate'][ancestry]['male']
        female_names = app.config['ancestry_generate'][ancestry]['female']
        non_binary_names = male_names + female_names
        generated_names = sample(non_binary_names, count)
    else:
        generated_names = sample(app.config['ancestry_generate'][ancestry][gender], count)

    # Apply prefix and suffix to each generated name
    modified_names = [f"{prefix} {name} {suffix}" for name in generated_names]
    return modified_names

if __name__ == '__main__':
    # Load dataset and start Flask application.
    with open('names.yaml', 'r') as yaml_file:
        app.config['ancestry_generate'] = yaml.safe_load(yaml_file)
    app.run(host='0.0.0.0', port='2224', debug=True)

