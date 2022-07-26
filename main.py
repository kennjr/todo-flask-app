from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# the __name__ creates a flask app that's named after the file it's in i.e main
app = Flask(__name__)
# the line below configures the flask app to the specified db
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://demo_user:password@localhost:5432/todo_db"
# the line below links SQLAlchemy to the flask app
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todos(db.Model):
    __tablename__ = 'todos'
    pk = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(), nullable=False)


@app.route('/')
def index():

    data = Todos.query.all()
    return render_template('index.html', data=data)
