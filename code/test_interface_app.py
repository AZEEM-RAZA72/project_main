from flask import Flask, render_template, redirect, request, flash,session
from database import User, add_to_db, open_db

app = Flask(__name__)
app.secret_key = 'thisissupersecrectkeyforsample'

@app.route("/")
def index():
    # You can fetch language options from a database or a list
    languages = ["English", "Spanish", "French", "German", "Italian"]
    return render_template("index.html", languages=languages)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print("Email=>",email)
        print("Password=>",password)
        if len(email) == 0 and len(password) == 0:
            flash('credentials cannot be empty', 'error')
            return redirect('/login')
        try:
            db = open_db()
            user = db.query(User).filter_by(email=email,password=password).first()
            if user:
                session['isauth'] = True
                session['email'] = user.email
                session['id'] = user.id
                session['username'] = user.username
                db.close()
                flash('login successfull','success')
                return redirect('/') 
            else:
                flash('email or password is wrong','danger')
        except Exception as e:
            flash(f'Error: {e}','danger')    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username') 
        email = request.form.get('email')
        password = request.form.get('password1')
        cpassword = request.form.get('password2')
        print(username,email,password,cpassword)
       
        if len(username)==0 or len(email)==0 or len(password)==0 or len(cpassword)==0:
            flash("All fields are required", 'error')   
            return redirect('/register') #reload the page
        try:
            user=User(username=username, email=email, password=password)
            add_to_db(user)
            flash("Account created", 'success')
            return redirect('/login')
        except Exception as e:
            flash(f"Error {e}", 'error')
            return redirect('/register')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
