#! /usr/bin/env python3
# james rogers | james.levi.rogers@gmail.com

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ancestries=['Human', 'Elf', 'Dwarf'])

@app.route('/names', methods=['POST'])
def names():
    ancestry = request.form.get('ancestry', 'Human').capitalize()
    gender = request.form.get('gender', 'male').lower()

    count_str = request.form.get('count', '5')

    if not count_str.isdigit():
        return redirect(url_for('index'))

    count = int(count_str)
    
    if count <= 0 or count > 50:
        return redirect(url_for('index'))
    if ancestry not in ['Human', 'Elf', 'Dwarf']:
        return redirect(url_for('index'))
    if gender not in ['male', 'female']:
        return redirect(url_for('index'))

    return render_template('names.html', names=['boby'])
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2224, debug=True)
