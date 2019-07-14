from flask import Flask, render_template, request, url_for, redirect, request, session, flash
from database import auth_user, add_user, add_story
app = Flask(__name__)
app.secret_key = "jrg;quoeiohqei833y2y8h"

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template("index1.html")
    else:
        username = request.form['username']
        password = request.form['password']
        # name = request.form['name']
        role = 0
        add_user(username,password,role)
        session['user_object'] = True
        session["username"] = username
   
        # check if the post request has the file part
        
        return redirect(url_for("home"))
    return render_template("index.html")

@app.route("/signup", methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template("sign_up.html")
    else:
        username = request.form['username']
        password = request.form['password']
        # name = request.form['name']
        role = 0
        add_user(username1,password1,role)
        session['user_object'] = True
        session["username"] = username
   
        # check if the post request has the file part
        
        return redirect(url_for("home"))

@app.route("/submit", methods=['GET', 'POST'])
def submite_story():
    if request.method == 'GET':
        return render_template ("submit.html")
    else:
        title= request.form['title']
        story= request.form['story']
        name=session["username"]
        add_story(name,title,story)
        return redirect(url_for("submit"))



if __name__ == '__main__':
    app.run(debug=True)

