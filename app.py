from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'sos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

#Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('index.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')

#Shop
@app.route('/shop')
def shop():
    return render_template('shop.html')

#Solution
@app.route('/solution')
def solution():
    return render_template('solution.html')
# Articles
@app.route('/stories')
def stories():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get the pending stories // to be changed to stories afterwards //
    result = cur.execute("SELECT * FROM pendingStories")

    story = cur.fetchall()

    if result > 0:
        return render_template('stories.html', story=story)
    else:
        msg = 'No stories Found'
        return render_template('stories.html', msg=msg)
    # Close connection
    cur.close()

def clever_function(body):
    body = body[3:25]
    return body

#Single storie
@app.route('/stories/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get stories // again to be changed to only stories
    result = cur.execute("SELECT * FROM pendingStories WHERE id = %s", [id])

    story = cur.fetchone()

    return render_template('blog_details.html', story=story)


# Register Form Class
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get stories
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    result = cur.execute("SELECT * FROM pendingStories WHERE author = %s", [session['username']])

    pendingStories = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', pendingStories=pendingStories)
    else:
        msg = 'No Stories Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

# Story Form Class
class StoryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add story
@app.route('/add_story', methods=['GET', 'POST'])
@is_logged_in
def add_story():
    form = StoryForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO pendingStories(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Story Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


# Edit Article
@app.route('/edit_story/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_story(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM pendingStories WHERE id = %s", [id])

    story = cur.fetchone()
    cur.close()
    # Get form
    form = StoryForm(request.form)

    # Populate article form fields
    form.title.data = story['title']
    form.body.data = story['body']
        
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE pendingStories SET title=%s, body=%s WHERE id=%s",(title, body, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('story Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_story/<string:id>', methods=['POST'])
@is_logged_in
def delete_story(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM pendingStories WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Story Deleted', 'success')

    return redirect(url_for('dashboard'))

#checkout
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
    
#products
@app.route('/p1')
def p1():
    return render_template("product1.html")

@app.route('/p2')
def p2():
    return render_template("product2.html")

@app.route('/p3')
def p3():
    return render_template("product3.html")

@app.route('/p4')
def p4():
    return render_template("product4.html")

@app.route('/p5')
def p5():
    return render_template("product5.html")

@app.route('/p6')
def p6():
    return render_template("product6.html")

@app.route('/p7')
def p7():
    return render_template("product7.html")

@app.route('/p8')
def p8():
    return render_template("product8.html")

@app.route('/p9')
def p9():
    return render_template("product9.html")

@app.route('/p10')
def p10():
    return render_template("product10.html")

@app.route('/p11')
def p11():
    return render_template("product11.html")

@app.route('/p12')
def p12():
    return render_template("product12.html")

app.jinja_env.globals.update(clever_function=clever_function)
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
