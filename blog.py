"""
Gerekli modüller için pip install komutları
- pip install Flask-WTF
- pip install flask-mysqldb
- pip install passlib
"""
from forms import RegisterForm, LoginForm 
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
#from datetime import datetime
#today = datetime.today()
#now = datetime.strftime(today, format="%Y-%m-%dT%H:%M:%S")

app = Flask(__name__)

# MySQL Configirasyonu bknz https://flask-mysqldb.readthedocs.io/en/latest/
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "projectflask"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
app.secret_key = "EDEL" #Flash mesajlarını yayınlamamız için secret key gerekiyor.

#Ana Sayfa
@app.route('/')
def main():
    articles = [
        {"id":1, "title":"Deneme1", "content":"Deneme1 içerik"},
        {"id":2, "title":"Deneme2", "content":"Deneme2 içerik"},
        {"id":3, "title":"Deneme3", "content":"Deneme3 içerik"}
    ]
    return render_template("index.html", articles = articles)

#Hakkında sayfası
@app.route("/about")
def about():
    return render_template("about.html")

#Login İşlemi
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM users where username = %s"
        result = cursor.execute(sorgu, (username,))
        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if password_entered == real_password:
                flash("Giriş yaptınız", "success")
                # Session kontrolünü yapıyoruz
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("main"))
            else: # Parola yanlışsa
                flash("Parolanız yanlış!!!", "danger")
                return redirect(url_for("login"))
        else:
            # Kullanıcı yoksa   
            flash("Böyle bir kullanıcı bulunmuyor!!!", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)

# Kayıt sayfası oluşturuyoruz
@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate(): # POST request ise url_for ile main'e yönlendiriyoruz.
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data) # Şifrelemek istersek sha256_crypt.encrypt() fonksiyonunu kullanmalıyız.
        # Phpmyadmin üzerinde işlem yapmak için cusor oluşturuyoruz.
        cursor = mysql.connection.cursor()
        # SQL Sorgumuz
        sorgu = "INSERT into users(name,username,email,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,username,email,password)) # Demet olarak execute ediyoruz
        mysql.connection.commit() # Veri tabınındaki bilgileri güncellemiş olduk. Silme, ekleme gibi durumlarda
        cursor.close()
        #layout içerisine dahil ettiğimiz flash message burada veriyoruz
        flash("Başarıyla Kayıt Oldunuz.", "success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)

# Logout işlemi
@app.route("/logout")
def logout():
    session.clear() # Sessionu temizliyoruz
    return redirect(url_for("main"))

# Dashboard için
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Dinamik URL Tanımlama
@app.route('/article/<string:id>')
def detail(id):
    return "Article Id:" + id

if __name__ == "__main__":
    app.run(debug=True)