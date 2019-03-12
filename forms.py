from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from flask import redirect, url_for, session, flash

# User register form (WTF formlarını Flask ile uyumunu kontrol et)
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators = [validators.Length(min=4, max=25)])
    username = StringField("Kullanıcı Adı", validators = [validators.Length(min=5, max=35, message="Geçerli bir kullanıcı                                                                           adı yazınız!")])
    email = StringField("Email Adresi", validators = [validators.Email(message="Lütfen geçerli bir email adresi giriniz!")])
    password = PasswordField("Parola", validators = [validators.DataRequired(message="Lütfen bir parola belirleyin!!!"),
                                                    validators.EqualTo(fieldname="confirm", message="Parolanız uyuşmuyor!!!")])
    confirm = PasswordField("Parola Doğrula")

class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = StringField("Parolanız")
    pass

# kullanıcı girişi kontrolü için flask decorator'ı http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görmek için giriş yapın!", "danger")
            return redirect(url_for("login"))
    return decorated_function