#base conda interpreter

from flask import Flask, render_template, request, redirect, url_for, session, flash
import Fetchtasks as ft
import Fetchusers as fu

app = Flask(__name__, template_folder="templates")
app.secret_key = "super secret key"

con = fu.connection()
cursor = con.cursor(dictionary=True)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    user, password = request.form["username"], request.form["password"]
    if (fu.verify(cursor, user, password)):
      id = fu.getId(cursor, user)
      session['loggedin'] = True
      session['username'] = id
      return redirect(url_for("home"))
    else:
      return redirect(url_for("login"))
  else:
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

  if request.method == "POST":
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    if (fu.createAccount(cursor, name, username, password)):
      flash('Successfully created account')
      con.commit()
      return redirect(url_for("login"))
    else:
      flash('Failed to create account ! Try Again !')
      return redirect(url_for("register"))
  else:
    return render_template("register.html")


@app.route("/home")
def home():
  username = session['username']
  tasks = ft.getDetails(cursor, username)
  return render_template("home.html",
                         tasks=tasks,
                         id=username,
                         name=fu.getName(cursor, username))


@app.route("/add", methods=["POST"])
def add():
  task = request.form['task']
  ft.addDetails(cursor, task, session['username'])
  return redirect(url_for("home"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
  tasks = ft.getDetails(cursor, session['username'])
  task = tasks[index]
  if request.method == "POST":
    ft.updateDetails(cursor, request.form["task"], task["todoid"])
    return redirect(url_for("home"))
  else:
    return render_template("edit.html", task=task, index=index)


@app.route("/check/<int:index>")
def check(index):
  tasks = ft.getDetails(cursor, session['username'])
  ft.markUpdate(cursor, tasks[index]['todoid'])
  return redirect(url_for("home"))


@app.route("/delete/<int:index>")
def delete(index):
  tasks = ft.getDetails(cursor, session['username'])
  ft.deleteItem(cursor, tasks[index]['todoid'])
  return redirect(url_for("home"))


@app.route("/logout")
def logout():
  con.commit()
  session.pop('loggedin', None)
  session.pop('username', None)
  return redirect(url_for('login'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
