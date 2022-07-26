from flask import Flask, render_template

# the __name__ creates a flask app that's named after the file it's in i.e main
app = Flask(__name__)

@app.route('/')
def index():
    data = [{'description': 'Todo one'}, {'description': 'Todo two'}, {'description': 'Todo three'}]
    return render_template('index.html', data=data)
