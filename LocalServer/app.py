"""
Created on 7/7/2021

Server that is to be displayed to the user with their personal attack stats.

"""

from flask import Flask, render_template, request, redirect, session
from webbrowser import *
from statCompiler import *
from hashPassword import *
from lsDatabase import *
import secrets


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config['SECRET_KEY'] = secrets.token_hex()

@app.route("/")
def default_page():
    return redirect("/userLogin")

@app.route("/userLogin", methods = ['GET', 'POST'])
def login_page():
    createDB()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if isPwd(username, password):
            session['user'] = username
            return redirect("/userstatistics")
        else:
            return "<h1 style='color:red;'> Incorrect username or password. <h1> "

    return render_template('login.html')


@app.route('/userstatistics', methods = ['GET', 'POST'])
def statistics():
    list = parse_data("/var/log/pfblockerng/unified.log")
  
    if 'user' in session:
        if request.method == 'POST':
            
            return redirect('/changeUser')

        return render_template('statistics.html', dayBlockNum = list[0], daylst = list[1], fiveDayBlockNum = list[2], 
                               fivedayslst = list[3], monthBlockNum = list[4], monthlst = list[5], top_ips_day = list[6], 
                               top_ips_fivedays = list[7], top_ips_month = list[8], domains=list[9], country_dict=list[10], 
                               html_str=list[11], html_dayhits=list[12], top_ips_all=list[13], timestamp_dict=list[14], 
                               num_of_attacks=list[15], last100=list[16])
    return redirect('/userLogin')

@app.route('/changeUser', methods = ['GET', 'POST'])
def changeUserPass():

    if 'user' in session:
        if request.method == 'POST':

            password = request.form['newPwd']
            
            updatePassword(password)
            return redirect("/userLogin")

        return render_template('change.html')
    
    return redirect('userLogin')

if __name__ == '__main__':
    createDB()
    app.run('0.0.0.0',debug=True)
