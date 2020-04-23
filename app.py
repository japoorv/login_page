from flask import Flask, render_template, redirect, url_for, request, jsonify
from flaskext.mysql import MySQL
import json
from config import set_config

app = Flask(__name__)
set_config(app)

mysql=MySQL()
mysql.init_app(app)

@app.route("/signme",methods=['POST'])
def checksignup():
    msg=None
    conn=mysql.connect()
    cursor=conn.cursor()
    if (request.form['password']!=request.form['password_check']):
        return render_template('signup.html',msg="Passwords don't match")
    try :
        cursor.execute("insert into users(user,email,password) values('"+request.form['name']+"','"+request.form['email']+"','"+request.form['password']+"');")
        conn.commit()
    except :
        msg="Username Not Available"
        return render_template('signup.html',msg=msg)
    return render_template('login.html',msg='Sign Up successful')


@app.route("/login",methods=['POST'])
def checklogin():
    msg=None
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("select exists(select * from users where (user='"+request.form['name']+"' and password='"+request.form['password']+"'));")
    res=(cursor.fetchall())
    res=[[j for j in i] for i in res]
    if (int(res[0][0])==0):
        msg="Wrong Id/Password"
        return render_template('login.html',msg=msg)
    else :
        return "Welcome"

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

#@app.route("/handleUpload", methods=['POST'])


if __name__=='__main__':
        app.run()
