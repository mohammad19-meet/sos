from flask import Flask, render_template, request, url_for
from database import get_all_blogs, create_blog, one_blog, get_all_hotels, create_hotel, get_one_hotel
import os
from werkzeug import secure_filename


UPLOAD_FOLDER = '/home/students/Desktop/Labs/Project/y2l-individual-project/static/img'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif'])




app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/blogs')
def blog_page():
    blogs = get_all_blogs()
    return render_template("blogs.html", blogs = blogs)

@app.route('/blogs/<int:id>')
def full_page(id):
    vblog = one_blog(id)
    return render_template("blog.html",vblog = vblog)
@app.route('/hotels/<int:id>')
def full_page_hotel(id):
    vhotel = get_one_hotel(id)
    return render_template("hotel.html",vhotel = vhotel)
@app.route('/todo')
def todo():
    return render_template("todo.html")

@app.route('/submit', methods =["GET","POST"])
def submit():
    if request.method =="GET":
        return render_template("submit.html")
    else:
        name = request.form['name']
        author = request.form['author']
        date = request.form['date']
        short_desc = request.form['short_desc']
        photo = request.form['photo']
        long_desc = request.form['long_desc']
        bio = request.form['bio']
        pers_photo = request.form['pers_photo']
        bfile = request.files['file']
        if bfile and allowed_file(bfile.filename):
            filename = secure_filename(bfile.filename)
            savename= os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.mknod(savename)
            print("YO IT ME:", savename)
            bfile.save(savename)
            bfile = "/static/img/" + filename


        create_blog(name,author,date,short_desc,photo,long_desc, bio, pers_photo,bfile)
        return render_template("blogs.html")

@app.route('/submit_hotel', methods =["GET","POST"])
def submit_hotel():
    if request.method =="GET":
        return render_template('submit_hotel.html')
    else:
        name = request.form['name']
        hotel_date = request.form['hotel_date']
        hotel_desc = request.form['hotel_desc']
        price = request.form['price']
        hotel_photo = request.files['file']
        if hotel_photo and allowed_file(hotel_photo.filename):
            filename = secure_filename(hotel_photo.filename)
            savename= os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.mknod(savename)
            print("YO IT ME:", savename)
            hotel_photo.save(savename)
            hotel_photo = "/static/img/" + filename


        create_hotel(name, hotel_date, hotel_desc, price, hotel_photo)
        return render_template("hotels.html")

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/hotels')
def hotel_page():
    hotels = get_all_hotels()
    return render_template("hotels.html", hotels = hotels)

@app.route('/connect_4')
def connect():
    return render_template("connect.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)

