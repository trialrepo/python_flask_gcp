import datetime
import logging
import os
import socket

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


app = Flask(__name__)


def is_ipv6(addr):
    """Checks if a given address is an IPv6 address."""
    try:
        socket.inet_pton(socket.AF_INET6, addr)
        return True
    except socket.error:
        return False


# [START example]
# Environment variables are defined in app.yaml.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    user = db.Column(db.String(50), primary_key = True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Details(db.Model):
    first = db.Column(db.String(50))
    last  = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(10), primary_key = True)
    desc = db.Column(db.String(500))
    salary = db.Column(db.String(50))
    sign = db.Column(db.String(50))

@app.route('/')
def index():
 return render_template('index.html')

@app.route('/register',methods=['POST'])    
def register():
    if request.form:
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        user = User(user = username, password = password, email = email)
        db.session.add(user)
        db.session.commit()
        return render_template('index.html', message = "Succesfully registered. Please login to continue!")

@app.route('/login',methods=['POST'])    
def login():
     # read the posted values from the UI
    username = request.form['name']
    password = request.form['password']
    user =User.query.filter_by(user = username, password = password).first()
    if user :
      return render_template('welcome.html', name = username)
    else:
      return render_template('index.html', error= "Please enter correct username and password")


@app.route('/desc',methods=['POST'])    
def  userdetails():
     # read the posted values from the UI
    first = request.form['first']
    last = request.form['last']
    address = request.form['address']
    phone = request.form['phone']
    desc = request.form['comment']
    sign = request.form['sign']
    salary = request.form['salary']
    details = Details(first = first, last = last, phone = phone, salary = salary, 
                      desc = desc , address = address ,sign = sign)
    db.session.add(details)
    db.session.commit()
    return render_template('welcome.html', message = "Details submitted!", first = first, 
           last = last, phone = phone , salary = salary,  address = address, sign = sign , comment = desc) 
      
@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
