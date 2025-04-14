from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Python/flask/project/todo/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example database model for Todo items
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    todo_list = Todo.query.all()
    # Show all todo
    return render_template('base.html', todo_list=todo_list)

@app.route("/add", methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    # Redirect after adding new todo
    return redirect(url_for('index'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        todo.completed = not todo.completed
        db.session.commit()
    # Redirect after updating the todo status
    return redirect(url_for('index'))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    # Redirect after deleting the todo item
    return redirect(url_for('index'))

def create_db():
    db.create_all()

if __name__ == '__main__':
    # create_db()  # Ensure DB and tables are created
    app.run(debug=True)
