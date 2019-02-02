from flask import Flask, request, redirect, render_template
import cgi
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/home')
def index():
    return render_template('home.html',title='User Sign-up')

#Password confimation function
def confirm(pwd, confirm_pwd):
    if pwd == confirm_pwd:
        return True
    else:
        return False

#Email validation function
def isValidEmail(email):
        if len(email) > 3 and len(email) < 21:
            if re.match("^.*?@.*?\.[a-z]{2,}?$", email) != None:
                return True
        return False
    
@app.route('/home', methods=['post'])
def signup():
    username = request.form['username']
    email = request.form['email']
    pwd = request.form['pwd']
    confirm_pwd = request.form['confirm_pwd']
    username_blank_error = ''
    username_length_error = ''
    username_space_error = ''
    email_invalid_error = ''
    pwd_blank_error = ''
    pwd_requirement_error = ''
    confirm_pwd_blank_error = ''
    confirm_error = ''
#Username    
    if username == '':
        username_blank_error = '*Required field'
    elif ' ' in username:
        username_space_error = "You can't put a space in your user name.  Come on man, get it together...'"
    else:
        if len(username) < 3 or len(username)> 20:
            username_length_error = 'Username must be between 3 and 20 characters'
#Email
    if email == '':
        pass 
    elif isValidEmail(email) == False :
        email_invalid_error = 'This email is invalid, try again.'
#Pwd
    if confirm_pwd == '':
        confirm_pwd_blank_error = '*Required field' 
    if pwd == '':
        pwd_blank_error = '*Required field'
    elif len(pwd) < 3 or len(pwd)> 20:
        pwd_requirement_error = 'Password must be between 3 and 20 characters'
    elif not confirm(pwd, confirm_pwd):
        confirm_error = 'You screwed up confirming your password, try again.'
        pwd = ''
        confirm_pwd = ''

#Render
    if  username_blank_error or username_length_error or username_space_error or email_invalid_error or pwd_blank_error or pwd_requirement_error or confirm_pwd_blank_error or confirm_error:
        return render_template('home.html', title='User Sign-up',
        username=username,
         email=email, pwd='', confirm_pwd='', username_blank_error=username_blank_error, username_length_error=username_length_error, 
         username_space_error=username_space_error, email_invalid_error=email_invalid_error, pwd_blank_error=pwd_blank_error, 
         pwd_requirement_error=pwd_requirement_error, confirm_pwd_blank_error=confirm_pwd_blank_error, confirm_error=confirm_error)
    else:
        username = username
        return redirect('/welcome?username={0}'.format(username))
@app.route("/welcome")
def welcome():
    username = request.args.get('username') 
    return render_template('welcome.html',title='Welcome',name = username)
    
app.run()