"""
Gerekli modüller için pip install komutları
- pip install Flask-WTF
- pip install flask-mysqldb
- pip install passlib
"""

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# MySQL Configirasyonu bknz https://flask-mysqldb.readthedocs.io/en/latest/
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flask_blog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# User register form
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators = [validators.Length(min=4, max=25)])


@app.route('/')
def main():
    articles = [
        {"id":1, "title":"Deneme1", "content":"Deneme1 içerik"},
        {"id":2, "title":"Deneme2", "content":"Deneme2 içerik"},
        {"id":3, "title":"Deneme3", "content":"Deneme3 içerik"}
    ]
    return render_template("index.html", articles = articles)

@app.route("/about")
def about():
    return render_template("about.html")

# Dinamik URL Tanımlama
@app.route('/article/<string:id>')
def detail(id):
    return "Article Id:" + id

if __name__ == "__main__":
    app.run(debug=True)