#! /usr/bin/env python3
# james rogers | james.levi.rogers@gmail.com

from random import sample
import yaml
from flask import Flask, redirect, render_template, request, url_for

# Initialize Flask application
app = Flask(__name__)

@app.route('/')
def index():
    # Display the main page with a dropdown of available ancestries.
    return render_template('index.html', ancestries=list(app.config['ancestry_generate'].keys()))

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

    # Render the names page with generated names.
    return render_template('names.html', names=generate_names_list(int(count_str), ancestry, gender))

def generate_names_list(count, ancestry, gender):
    """
    Fetch a random sample of names from the dataset based on given criteria.
    """
    return sample(app.config['ancestry_generate'][ancestry][gender], count)

if __name__ == '__main__':
    # Load dataset and start Flask application.
    with open('racegendernames.yaml', 'r') as yaml_file:
        app.config['ancestry_generate'] = yaml.safe_load(yaml_file)
    app.run(host='0.0.0.0', port='2224', debug=True)

