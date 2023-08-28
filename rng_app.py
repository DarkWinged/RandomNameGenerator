#! /usr/bin/env python3
# james rogers | james.levi.rogers@gmail.com

from random import sample
import yaml
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ancestries=list(app.config['ancestry_generate'].keys()))

@app.route('/names', methods=['POST'])
def names():
    ancestry = request.form.get('ancestry', 'Human').capitalize()
    
    if '-' in ancestry:
        parts = ancestry.split('-')
        new_parts = []
        for part in parts:
            new_parts.append(part.capitalize())
        ancestry = '-'.join(new_parts)

    gender = request.form.get('gender', 'male').lower()

    count_str = request.form.get('count', '5')

    if not count_str.isdigit():
        return redirect(url_for('index'))

    count = int(count_str)
    
    if count <= 0 or count > 50:
        return redirect(url_for('index'))
    if ancestry not in list(app.config['ancestry_generate'].keys()):
        return redirect(url_for('index'))
    if gender not in ['male', 'female']:
        return redirect(url_for('index'))
                        
    return render_template('names.html', names=generate_names_list(count, ancestry, gender))

def generate_names_list(count, ancestry, gender):
    return sample(app.config['ancestry_generate'][ancestry][gender], count)

if __name__ == '__main__':
    with open('racegendernames.yaml', 'r') as yaml_file:
        ancestor_generate = yaml.safe_load(yaml_file)

    app.config['ancestry_generate'] = ancestor_generate
    
    app.run(host='0.0.0.0', port='2224', debug=True)
