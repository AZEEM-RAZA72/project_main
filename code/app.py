from flask import Flask, render_template, redirect, request, flash,session
from database import User, add_to_db, open_db


app = Flask(__name__)
app.secret_key = 'thisissupersecrectkeyforsample'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print("Email =>", email)
        print("Password =>", password)
        # logic
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        print(username, email, password, cpassword)
        # logic
        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(cpassword) == 0:
            flash("All fields are required", 'danger')
            return redirect('/register')
        user = User(username=username, email=email, password=password)
        add_to_db(user)
    return render_template('register.html')

@app.route('file/upload/', methods=['GET', 'POST'])
def file_upload():
    return render_template('upload.html')

@app.route('/file/list', methods=['GET', 'POST'])
def file_list():
    return render_template('display_list.html')

@app.route('file/<int:file_id>/view')
def func_name(id):
    return render_template('view_file.html')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 