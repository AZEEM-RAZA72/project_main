from flask import Flask, render_template, redirect, request, flash
from flask import Response, stream_with_context
import time

app = Flask(__name__)
app.secret_key = 'thisissupersecrectkeyforsample'

# Dummy function to generate streaming text data
def generate_text_data():
    for i in range(1, 6):
        time.sleep(1)  # Simulation of some processing time
        yield f"Line {i}\n"

# Route for the page that receives streaming text data
@app.route('/')
def streaming_text():
    return Response(stream_with_context(generate_text_data()), content_type='text/plain')

# Your existing routes for user authentication

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
        # Your existing logic for user authentication
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        print(username, email, password, cpassword)
        # Your existing logic for user registration
        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(cpassword) == 0:
            flash("All fields are required", 'danger')
            return redirect('/register')
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
