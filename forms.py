from wtforms import Form, StringField, TextAreaField, PasswordField, validators

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