from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import time
import psutil
import multiprocessing
import socket
import os
import requests

app = Flask(__name__)

dbstring = os.environ["DBSTRING"]

app.config['SQLALCHEMY_DATABASE_URI'] = dbstring
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Booklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200),nullable=False) 
    resenha = db.Column(db.Text)
    def __repr__(self):
        return f'<Booklist {self.name}>'


with app.app_context():
    db.create_all()
    


def aws_get_metadata():
    URL_AZ = 'http://169.254.169.254/latest/meta-data/placement/availability-zone'
    URL_HOSTNAME = 'http://169.254.169.254/latest/meta-data/hostname'
    resp_az = requests.get(URL_AZ)
    resp_hostname = requests.get(URL_HOSTNAME)
    meta_fields = {
        "AZ": resp_az.text.split('\n'),
        "hostname": resp_hostname.text.split('\n')
    }
    return meta_fields

def cpu_load(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        #render_template('index.html')
        pass

@app.route('/books')
def index():
    books = db.session.execute(db.select(Booklist).order_by(Booklist.name)).scalars()
    return render_template("booklist.html", books=books)


@app.route('/books/create', methods=['GET', 'POST'])
def books_create():
    if request.method =="POST":
        book=Booklist(
            name=request.form['name'], 
            author=request.form['author'], 
            resenha=request.form['resenha'],)
        db.session.add(book)
        db.session.commit()
        return render_template("book.html",book=book)
    return render_template("bookcreate.html")
    
    
    
@app.route('/show_cpu')
def show_cpu():
    cpu = psutil.cpu_percent(4)
    return render_template('show_cpu.html', cpu=cpu)


@app.route('/', methods=['GET', 'POST'])
def form():
    
    info = aws_get_metadata()
    if request.method == 'POST':
       
        duration = int(request.form['duration'])
        for _ in range(0, multiprocessing.cpu_count()):
            process = multiprocessing.Process(target=cpu_load, args=(duration,))
            process.start()
        return(render_template('form.html',duration=duration, hostname=info["hostname"], AZ=info["AZ"]))    
    
    return render_template('form.html', hostname=info["hostname"], AZ=info["AZ"])

if __name__ == '__main__':
    
    app.run(debug=True, port=5000, host='0.0.0.0')
