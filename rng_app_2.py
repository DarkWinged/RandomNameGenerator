from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ancestries=list(app.config['ancestor_origin'].keys()))

@app.route('/names', methods=['POST'])
def names():
    ancestry = request.form.get('ancestry', 'Human').capitalize()
    gender = request.form.get('gender', 'male').lower()
    count = int(request.form.get('count', '5'))

    selected_names = app.config['ancestor_origin'].get(ancestry, {}).get(gender, [])

    generated_names = selected_names[:count]

    return render_template('names.html', generated_names=generated_names)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2224', debug=True)

