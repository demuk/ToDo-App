from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


# initialising a model 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.Datetime, default = datetime.utcnow)


    # function to return a string when an element is created
    def __repr__(self):
        return '<Task %r>' % self.id
        

@app.route('/home')
def home():
    return render_template('index.html')



if __name__  == '__main__':
    app.run(debug=True)