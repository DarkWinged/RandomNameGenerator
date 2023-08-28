#! /usr/bin/env python3
#james rogers|james.levi.rogers@gmail.com

from flask import Flask, redirect, render_template, request
import yaml

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ancestries=list(app.config['ancestry_generate'].keys()))

@app.route('/names', methods=['POST'])
def names():
    ancestry = request.form.get('ancestry', 'Human').capitalize()
    gender = request.form.get('gender', 'male').lower()
    count = int(request.form.get('count', '5'))
    return 'To do: make a names.html and names.css'

if __name__ == '__main__':
    with open('racegendernames.yaml', 'r') as yaml_file:
        ancestor_generate = yaml.safe_load(yaml_file)
    app.config['ancestry_generate'] = ancestor_generate
    
    app.run(host='0.0.0.0', port='2224', debug=True)

