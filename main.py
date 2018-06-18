from flask import Flask, request, redirect, render_template,session, url_for
import re
import os
import jinja2


app = Flask (__name__)
app.config['DEBUG'] = True
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'secret key'

template_dir = os.path.join(os.path.dirname(__file__), "templates")  
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

@app.route("/", methods = ['GET', 'POST'])
def login():
    title = 'Signup!'
    username = ''
    email = ''
    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        email = request.form['email']
        session['username'] = username
        
        if (len(username) <4) or (len(username)>20):
            username_error = "Username must be between 3 and 20 characters fool!"
            username = ''

        if (len(password) <4) or (len(password) >20):
            password_error = "Keep your password to between 3 and 20 characters idiot!"
        elif password != verify_password:
            verify_password_error = "You entered two different passwords fool!"
        if (email != '') and (not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)):
            email_error = "You entered a messed up email!"
            email = ''

        if (not username_error) and (not password_error) and (not verify_password_error) and (not email_error):
            return redirect(url_for('.welcome', username= username))
    return render_template('login_form.html', title = title, username_error = username_error, password_error = password_error, verify_password_error = verify_password_error, email_error = email_error, username = username, email = email)

@app.route("/welcome")
def welcome():
    title = 'Welcome fool!'
    username = session['username']
    return render_template('welcome.html', title = title, username= username)

if __name__ == '__main__':
    app.run()