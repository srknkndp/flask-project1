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

# User register form (WTF formlarını Flask ile uyumunu kontrol et)
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators = [validators.Length(min=4, max=25)])
    username = StringField("Kullanıcı Adı", validators = [validators.Length(min=5, max=35)])
    email = StringField("Email Adresi", validators = [validators.Email(message="Lütfen geçerli bir email adresi giriniz!")])
    password = PasswordField("Parola", validators = [validators.DataRequired(message="Lütfen bir parola belirleyin!!!"),
                                                    validators.EqualTo(fieldname="confirm", message="Parolanız uyuşmuyor!!!")])
    confirm = PasswordField("Parola Doğrula")

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

# Kayıt sayfası oluşturuyoruz
@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate(): # POST request ise url_for ile main'e yönlendiriyoruz.
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data # Şifrelemek istersek sha256_crypt.encrypt() fonksiyonunu kullanmalıyız.
        # Phpmyadmin üzerinde işlem yapmak için cusor oluşturuyoruz.
        cursor = mysql.connection.cursor()
        # SQL Sorgumuz
        sorgu = "Insert into users(name,username,email,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,username,email,password)) # Demet olarak execute ediyoruz
        mysql.connection.commit() # Veri tabınındaki bilgileri güncellemiş olduk. Silme, ekleme gibi durumlarda
        cursor.close()
        return redirect(url_for("main"))
    else:
        return render_template("register.html", form=form)

# Dinamik URL Tanımlama
@app.route('/article/<string:id>')
def detail(id):
    return "Article Id:" + id

if __name__ == "__main__":
    app.run(debug=True)