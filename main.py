import sys

from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# the __name__ creates a flask app that's named after the file it's in i.e main
# from werkzeug.utils import redirect
from werkzeug.utils import redirect

app = Flask(__name__)
# the line below configures the flask app to the specified db
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://demo_user:password@localhost:5432/todo_db"
# CORS(app)
# the line below links SQLAlchemy to the flask app
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todos(db.Model):
    __tablename__ = 'todos'
    pk = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)


@app.route('/')
def index():
    # new_data_id = 3
    # first_todo = Todos(pk=new_data_id, description="The fourth task")
    # second_todo = Todos(pk=new_data_id+1, description="The fifth task")
    # third_todo = Todos(pk=new_data_id+2, description="The sixth task")
    #
    # db.session.add_all([first_todo, second_todo, third_todo])
    # db.session.commit()
    data = Todos.query.order_by('pk').all()
    # for item in data:
    #     db.session.delete(item)
    # db.session.commit()
    return render_template('index.html', data=data)



# @app.route('/todos/create', methods=['POST'])
# def create_todo():
#     # get the data from the form
#     description = request.form.get('description')
#     # add the data to the server
#     todo_item = Todos(description=description)
#     db.session.add(todo_item)
#     db.session.commit()
#     return redirect(url_for('index'))
#     # return render_template("index.html")


@app.route('/todos/<pk>/delete', methods=['DELETE'])
def delete_todo_item(pk):
    body = {}
    try:
        deleted_todo = Todos.query.get(pk)
        db.session.delete(deleted_todo)
        db.session.commit()
        body = {'status': True}
    except:
        print(sys.exc_info())
        db.session.rollback()
        body = {'status': False}
    finally:
        db.session.close()
    return jsonify(body)


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed(todo_id):
    todo = Todos.query.get(todo_id)
    if todo:
        # if we get an item with the id passed int the route then we can make an attempt to process it
        try:
            completed = request.get_json()['completed']
            todo.completed = completed
            db.session.commit()
        except:
            db.session.rollback()
            # the print statement below will give us more info on what caused the error
            print(sys.exc_info())
            # we're returning the todo_obj back to the user as a json_obj
        finally:
            # this should happen regardless
            db.session.close()
        return redirect(url_for('index'))
    else:
        db.session.close()


@app.route('/todos/create', methods=['POST'])
def create_todo():
    # the body var is what we'll use to send data back to the user
    body = {}
    error = False
    try:
        # we're getting the data from the request
        description = request.get_json()['description']
        # creating a new todo_item that'll be added to the db
        todo = Todos(description=description)
        db.session.add(todo)
        db.session.commit()
        body = {'description': todo.description}
    except:
        error = True
        db.session.rollback()
        # the print statement below will give us more info on what caused the error
        print(sys.exc_info())
        # we're returning the todo_obj back to the user as a json_obj
    finally:
        # this should happen regardless
        db.session.close()
    if not error:
        return jsonify(body)
    else:
        return jsonify({'error': "An error occurred"})


if __name__ == '__main__':
    # set the debug to true for the app to be restarted every time we make changes
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
