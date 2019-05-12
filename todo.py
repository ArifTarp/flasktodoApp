from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Lenovo/Desktop/Todo App/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    veriler = Todo.query.all() # sözlük halinde veritabanından gelir veriler
    if veriler != 0:
        return render_template("index.html",data = veriler)
    else:
        return render_template("index.html")
    

@app.route("/add",methods=["POST"]) # sadece post requeste izin verdik
def add():
    newTitle = request.form.get("title") # request.form.title böyle yazamayız çünkü wtf formu değil
    newTodo = Todo(title = newTitle,complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def complete(id):
    güncellenecek = Todo.query.filter_by(id=id).first() # idye göre ilk değeri alır .first()
    """if güncellenecek.complete:
        güncellenecek.complete = False
        db.session.add(güncellenecek)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        güncellenecek.complete = True
        db.session.add(güncellenecek)
        db.session.commit()
        return redirect(url_for("index"))"""
    güncellenecek.complete = not güncellenecek.complete
    db.session.add(güncellenecek)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    silinecek = Todo.query.filter_by(id=id).first() # silinecek todonun bana bütün bilgilerini getirdi
    db.session.delete(silinecek)
    db.session.commit()
    return redirect(url_for("index"))


if __name__=="__main__":
    db.create_all() # oluşturulmak istenen tablolar varsa bir daha oluşturmaz
    app.run(debug=True)



