from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
todo = Flask(__name__)
todo.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
todo.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(todo)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)    
    title = db.Column(db.String(50), nullable=False)    
    desc = db.Column(db.String(300), nullable=False)    
    date_made = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}" 

@todo.route("/", methods=['GET','POST'])
def homepage():
    if request.method=='POST':
        title_todo = request.form.get('title')
        desc_todo = request.form.get('desc')
        todo = Todo(title=f"{title_todo}", desc=f"{desc_todo}")
        db.session.add(todo)
        db.session.commit()
    
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo = alltodo)

@todo.route("/delete/<int:sno>")
def delete(sno):
    deleted = Todo.query.filter_by(sno=sno).first()
    db.session.delete(deleted)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    todo.run(debug=True, port=2648)