"""
Created on Mon Jun 28 

@author: Ace Abdulrahman
"""
from flask import Flask, render_template, request, redirect, url_for, session
from database import *
from adminCreds import truUsername, truPasswrd



app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config['SECRET_KEY'] = secrets.token_hex()

def crctPwd(usr,pwd):
    return usr == truUsername and pwd == truPasswrd

@app.route('/')
def IPList():
    msg=''
    token = request.args.get('token')
    if not token:
        msg = ['403', 'Forbidden', "You don't have permission to access this server"]
        return render_template('error.html', msg=msg)
    try:
        if isToken(token):
            with open('IP_address.txt', 'r') as f: 
                return render_template('content.html', text=f.read())
        msg = ['401', 'Unauthorized', "Invalid credentials. Access Denied."]
        return render_template('error.html', msg=msg)
    except:
        return "<h1 style='color:red;'> 403: Page not found <h1> "

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    msg=""
    if 'admin' in session:
        if request.method == 'POST' :
            email = request.form["email"]
            description = request.form['desc']
            genToken(email, description)
            msg= "User added"

        return render_template('admin.html', rows=showTokens(), msg=msg)
    return redirect(url_for('adminLogin'))

@app.route('/StingarAdmin', methods = ['GET', 'POST'])
def StingarAdmin():
    msg=""
    if 'coadmin' in session:
        if request.method == 'POST' :
            email = request.form["email"]
            description = request.form['desc']
            genToken(email, description)
            msg= "User added"

        return render_template('coadmin.html', rows=showTokens(), msg=msg)
    return redirect(url_for('adminLogin'))


@app.route('/adminLogin', methods = ['GET', 'POST'])
def adminLogin():
    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        if isPwd(username, password):
            if username == 'admin':
                session['admin'] = username
                return redirect(url_for('admin'))
            session['coadmin']= username
            return redirect(url_for('StingarAdmin', user = username))
        msg="Incorrect username or password"
    return render_template("adminLogin.html", msg=msg)

@app.route('/delete_token', methods=["POST"])
def delete_token():
    row = request.args.get('row')
    deleteUser(row)
    return redirect(url_for('admin'))

@app.route('/update_token', methods=["POST"])
def update_token():
    email =request.form.get("email", "")
    desc =request.form.get("desc", "")
    date =request.form.get("date", "")
    token =request.form.get("token", "")
    row = request.args.get('row')
    updateTable(email, desc, date, token, row)
    return redirect(url_for('admin'))

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    if 'admin' in session:
        msg=""
        if request.method == 'POST' :
            email = request.form["email"]
            description = request.form['desc']
            password = request.form['password']
            confPassword = request.form['ConfPassword']
            if password != confPassword:
                msg="Passwords don't match"
                return render_template('settings.html', msg=msg, rows = showAdmins())
            addAdmin(email,description,password)
            msg="Admin Added"
        return render_template('settings.html', msg=msg, rows = showAdmins())
    return redirect(url_for('adminLogin'))

@app.route('/delete_admin', methods=["POST"])
def delete_admin():
    row = request.args.get('row')
    delAdmin(row)
    return redirect(url_for('settings'))

@app.route('/update_admin', methods=["POST"])
def update_admin():
    email = request.form.get("email", "")
    desc =request.form.get("desc", "")
    date =request.form.get("date", "")
    #pwd =request.form.get("pwd", "")
    row = request.args.get('row')
    updateAdmin(email, desc, date, row)
    return redirect(url_for('settings'))

@app.route('/update_password', methods= ["GET","POST"])
def update_password():
    #oldPwd = request.form.get('oldPwd')
    msg=""
    if 'coadmin' in session:
        user = session['coadmin']
        if request.method == "POST":
            newPwd = request.form.get('newPwd')
            confPwd = request.form.get('confPwd')
            if newPwd==confPwd:
                changePwd(newPwd,user)
                msg="Password Updated"
                return render_template('pwdUpdate.html', msg = msg)
            msg = 'Update Failed. Try Again'
        return render_template('pwdUpdate.html', msg = msg)   


    if 'admin' in session:
        user = session['admin']
        if request.method == "POST":
            newPwd = request.form.get('newPwd')
            confPwd = request.form.get('confPwd')
            if newPwd==confPwd:
                changePwd(newPwd, user)
                msg="User Added"
                return render_template('pwdUpdate.html', msg = msg)
            

        return render_template('pwdUpdate.html')   

    return redirect(url_for('adminLogin'))

if __name__ == '__main__':
    adminDB()
    createDB()
    app.run('0.0.0.0',debug=True)
