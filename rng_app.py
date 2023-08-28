#! /usr/bin/env python3
#james rogers|james.levi.rogers@gmail.com

from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ancestries=['Human','Elf','Dwarf']) # replace the static list with a list of the keys in app.config[<data_variable_name>]

@app.route('/names', methods=['POST'])
def names():
    ancestry = request.form.get('ancestry', 'Human').capitalize()
    gender = request.form.get('gender', 'male').lower()
    count = int(request.form.get('count', '5'))
    return 'To do: make a names.html and names.css'

if __name__ == '__main__':
    #load in the data from the yaml
    #save the data in app.config[<data_variable_name>]
    app.run(host='0.0.0.0', port='2224', debug=True)

