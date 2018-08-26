from flask import Flask, render_template,  flash, redirect, url_for, session, logging, request, jsonify
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateTimeField
from passlib.hash import pbkdf2_sha256
from datetime import datetime


app = Flask(__name__) # APP'i oluşturuyoruz.
app.secret_key = "edizbarlas"

app.config["MYSQL_DATABASE_HOST"] = "localhost" # Sunucu adresi
app.config["MYSQL_DATABASE_USER"] = "root" # MySQLDB'yi kurduğumuzda User ve Password bu şekilde geliyor.
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "projectflask" # MySQL üzerindeki veritabını ismi.
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# MYSQL BAĞLANTISI
mysql = MySQL()
mysql.init_app(app)

# Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators=[validators.Length(min=4, max=25), validators.DataRequired(message="Bu alanı doldurmak zorundasınız.")])
    username = StringField("Kullanıcı adı", validators=[validators.Length(min=5, max=35), validators.DataRequired("Bu alanı boş bırakamazsınız")])
    email = StringField("Email Adresi", validators=[validators.Email(message="Lütfen geçerli bir email adresi giriniz!")])
    password = PasswordField("Parola: ", validators=[validators.DataRequired(message="Lütfen parola belirleyiniz!"), validators.EqualTo(fieldname="confirm", message="Parolanız uyuşmuyor!")])
    confirm = PasswordField("Parola Doğrula")
    date = str(datetime.now())
    confirm_date = DateTimeField(default=date, format="%Y-%m-%d %H:%M")

# @app.route("/")
# def homepage():
#     return render_template("freehomepage.html")

# @app.route("/testpage")
# def testpage():
#     sayi = 10
#     sayi2 = 2
#     articles = {"Title":"Deneme", "Body": "Deneme 123", "Author":"Serkan Kındap"}
#     return render_template("testpage.html", number=[sayi, sayi2], articles=articles)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ipaddress = jsonify(request.remote_addr)
    return (ipaddress), 200

@app.route("/register", methods= ["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate(): # Form validate olup olmadığını kontrol ediyoruz
        name = form.name.data
        username = form.name.data
        email = form.email.data
        password = form.password.data # sha256_crypt şifreleme için kullanabilirsin
        confirm_date = form.confirm_date.data
        cursor = mysql.get_db().cursor()
        sorgu = "INSERT INTO users(name, username, email, password, confirm_date VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(name, username, email, password, confirm_date)) # Demet olarak gönderiyoruz ',' unutma
        mysql.get_db().commit() # Veri tabanındaki değişiklikler için commit yapmalısın.
        
        cursor.close() # Veritabanı güncellendikten sonra cursorı kapat.
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/articles/<string:id>")
def articles(id):   
    return render_template("articles.html", id=id)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

if __name__ == "__main__":
    app.run(debug=True) 