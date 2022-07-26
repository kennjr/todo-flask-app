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
    # new_data_id = 3
    # first_todo = Todos(pk=new_data_id, description="The fourth task")
    # second_todo = Todos(pk=new_data_id+1, description="The fifth task")
    # third_todo = Todos(pk=new_data_id+2, description="The sixth task")
    #
    # db.session.add_all([first_todo, second_todo, third_todo])
    # db.session.commit()
    data = Todos.query.all()
    return render_template('index.html', data=data)


if __name__ == '__main__':
    # set the debug to true for the app to be restarted every time we make changes
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
