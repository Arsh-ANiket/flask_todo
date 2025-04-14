from flask import Flask, render_template,request,redirect,url_for
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
    todo_list=Todo.query.all()
        # show all todo
    return render_template('base.html',todo_list=todo_list)

@app.route("/add",methods=['POST'])
def add():
    title=request.form.get('title')
    with app.app_context():
         new_todo=Todo(title=title, completed=False)
         db.session.add(new_todo)
         db.session.commit()
         # name of the func has to be passed in the url
         return redirect(url_for('index'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    with app.app_context():
        todo=Todo.query.filter_by(id=todo_id).first()
        todo.completed=not todo.completed
        db.session.commit()
         # name of the func has to be passed in the url
        return redirect(url_for('index'))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    with app.app_context():
        todo=Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
         # delete the todo item
        db.session.commit()
         # name of the func has to be passed in the url
        return redirect(url_for('index'))


def create_db():
    with app.app_context():  # Push application context
        db.create_all()

if __name__ == '__main__':
    create_db()  # Ensure DB and tables are created
    # creating a dummy data
    # with app.app_context():
    #     new_todo=Todo(title='Learn Flask', completed=False)
    #     db.session.add(new_todo)
    #     db.session.commit()  # Commit the new todo item to the database
    
    app.run(debug=True)
