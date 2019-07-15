from flask import Flask, render_template, request, url_for, redirect, request, session, flash
from database import auth_user, add_user, add_story, story_by_name
app = Flask(__name__)
app.secret_key = "jrg;quoeiohqei833y2y8h"

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template("index.html")
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

@app.route("/home")
def home1():
    return render_template("home.html")
#@app.route("/profile/<int:id>")
@app.route("/profile")
def profile():
    user=auth_user("shelly",1234)
    stories=story_by_name("shelly")
    return render_template("profile.html", user=user, stories=stories)
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
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method== 'GET':
        return render_template("sign_in.html")
    else:
        username = request.form['username']
        password = request.form['password']
        user=auth_user(username,password)
        session['user_object'] = True
        session["username"] = username

        return redirect(url_for("home"))



@app.route("/submit", methods=['GET', 'POST'])
def submite_story():
    if request.method == 'GET':
        return render_template ("submit.html")
    else:
        title= request.form['title']
        story= request.form['story']
        name="gorge"
        add_story(name,title,story)
        return render_template("thank.html")
@app.route("/thank")
def thank():
    return render_template("thank.html")



if __name__ == '__main__':
    app.run(debug=True)

