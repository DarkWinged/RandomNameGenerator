#! /usr/bin/env python3
#james rogers|james.levi.rogers@gmail.com

from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ancestries=['Human','Elf','Dwarf'])

@app.route('/names', methods=['POST'])
def names():
    ancestry = request.form.get('ancestry', 'Human').capitalize()
    gender = request.form.get('gender', 'male').lower()
    count = int(request.form.get('count', '5'))
    return render_template('names.html', names=['boby'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2224', debug=True)

