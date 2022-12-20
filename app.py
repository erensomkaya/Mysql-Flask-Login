from flask import Flask,render_template,redirect,request,url_for,flash
from wtforms import Form,StringField,PasswordField,TextAreaField,validators
from passlib.hash import sha256_crypt

from flask_mysqldb import MySQL

class Register(Form):

    user = StringField("İsim Soyisim : ",validators=[validators.length(min=3,max=20),validators.DataRequired()])
    username = StringField("Kullanıcı Adı : ",validators=[validators.length(min=3,max=20),validators.DataRequired()])
    email = StringField("E-mail : ",validators=[validators.email(message="E-mail boş bırakmayınız."),validators.DataRequired()])
    password= PasswordField("Parola : ",validators=[validators.length(min=3,max=20),validators.DataRequired(),validators.equal_to(fieldname="confirm",message="Parola eşleşmiyor.")])
    confirm = PasswordField("Parola Doğrula  : ",validators=[validators.length(min=3,max=20),validators.DataRequired()])

class Login(Form):

    username = StringField("Kullanıcı Adı : ",validators=[validators.DataRequired()])
    password = PasswordField("Parola : ",validators=[validators.DataRequired()])




app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = "eren"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "eren"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hakkımda")
def hakkımda():
    return render_template("hakkımda.html")

@app.route("/destek")
def destek():
    return render_template("destek.html")



@app.route("/register",methods = ["GET","POST"])
def register():
    form = Register(request.form)
    if request.method == "POST" and form.validate():

        user = form.user.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.confirm.data)
        cursor = mysql.connection.cursor()

        e = "Insert into kayitlar(user,username,email,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(e,(user,username,email,password))
        mysql.connection.commit()
        cursor.close()
        flash("Başarıyla kayıt oldunuz.","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)




@app.route("/login",methods = ["GET","POST"])
def login():
    form = Login(request.form)
    if request.method == "POST":


        username = form.username.data
        yeni_password = form.password.data

        cursor = mysql.connection.cursor()

        i = "Select * From kayitlar where username = %s "
        b = cursor.execute(i,(username,))
        if b>0:
            data = cursor.fetchone()
            l_password = data["password"]
            if sha256_crypt.verify(yeni_password,l_password):
                flash("Başarıyla Giriş Yaptınız.","success")
                return redirect(url_for("destek"))
            else:
                flash("Böyle bir parola mevcut değil . ","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı adı bulunmuyor.","danger")
            return redirect(url_for("login"))












    return render_template("login.html",form = form)


if __name__ =="__main__":
    app.run(debug=True)