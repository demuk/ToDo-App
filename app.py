from logging import debug
from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


# initialising a model 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    # function to return a string when an element is created
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/home', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/home')
        
        except:
            return 'Your Task could not be added!'


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()

        return redirect('/home')
    except:
        return 'There was an error deleting your task!!' 

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try: 
            db.session.commit()
            return redirect('/home')
        except:
            return 'There was an error updating the task'
    else:
        return render_template('update.html', task=task)



if __name__ == '__main__':
    app.run(debug=True)