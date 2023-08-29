
from random import sample
import yaml
from flask import Flask, redirect, render_template, request, url_for, session
from datetime import datetime, timedelta
import hashlib

# Initialize Flask application
app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

@app.before_request
def check_names_endpoint():
    if request.endpoint is None:
        return redirect(url_for('index'))

@app.route('/')
def index():
    # Retrieve stored choices from session, or use default values
    stored_ancestry = session.get('ancestry', 'Human')
    stored_gender = session.get('gender', 'male')
    stored_count = session.get('count', '5')
    stored_prefix = session.get('prefix', '')
    stored_suffix = session.get('suffix', '')
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

    # Store user's choices, prefix, and suffix in the session
    session['ancestry'] = ancestry
    session['gender'] = gender
    session['count'] = count_str
    session['prefix'] = prefix
    session['suffix'] = suffix

    # Render the names page with generated names.
    return render_template('names.html', names=generate_names_list(int(count_str), ancestry, gender, prefix, suffix))

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
    # Generate the secret key
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    secret_key = hashlib.sha256(current_time.encode()).hexdigest()
    app.config['SECRET_KEY'] = secret_key
    #session.permanent = True

    # Load dataset and start Flask application.
    with open('racegendernames.yaml', 'r') as yaml_file:
        app.config['ancestry_generate'] = yaml.safe_load(yaml_file)
    app.run(host='0.0.0.0', port='2224', debug=True)

