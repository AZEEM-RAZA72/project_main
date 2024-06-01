from flask import Flask, render_template, redirect, request, flash,session
from database import User, add_to_db, open_db
from myllm import query, correction_api
import json

app = Flask(__name__)
app.secret_key = 'thisissupersecrectkeyforsample'

'''
Microsoft David - English (United States) en-US
VM143:51 Microsoft Ravi - English (India) en-IN
VM143:51 Microsoft Heera - English (India) en-IN
VM143:51 Microsoft Mark - English (United States) en-US
VM143:51 Microsoft Zira - English (United States) en-US
VM143:51 Google Deutsch de-DE
VM143:51 Google US English en-US
VM143:51 Google UK English Female en-GB
VM143:51 Google UK English Male en-GB
VM143:51 Google español es-ES
VM143:51 Google español de Estados Unidos es-US
VM143:51 Google français fr-FR
VM143:51 Google हिन्दी hi-IN
VM143:51 Google Bahasa Indonesia id-ID
VM143:51 Google italiano it-IT
VM143:51 Google 日本語 ja-JP
VM143:51 Google 한국의 ko-KR
VM143:51 Google Nederlands nl-NL
VM143:51 Google polski pl-PL
VM143:51 Google português do Brasil pt-BR
VM143:51 Google русский ru-RU
VM143:51 Google 普通话（中国大陆） zh-CN
VM143:51 Google 粤語（香港） zh-HK
VM143:51 Google 國語（臺灣） zh-TW
'''
lang_dict = {
    'american_english': 'en-US',
    'british_english': 'en-GB',
    'hindi': 'hi-IN',
    'spanish': 'es-ES',
    'french': 'fr-FR',
    'german': 'de-DE',
    'italian': 'it-IT',
    'japanese': 'ja-JP',
    'korean': 'ko-KR',
    'chinese': 'zh-CN',
    'russian': 'ru-RU',
    'portuguese': 'pt-BR',
    'dutch': 'de-De',
}

@app.route("/")
def index():
    # You can fetch language options from a database or a list
    languages = ["American English", "Australian English", "British English"]
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

@app.route('/train', methods=['GET', 'POST'])
def train():
    chapter = ''
    if 'isauth' not in session or not session.get('isauth'):
        return redirect('/login')
    if request.method == 'POST':
        chapter = request.form.get('chapter')
        lang = request.form.get('lang') 
        print(chapter, lang)
        result = query(chapter, lang)
        print(result.text)
        return render_template('train.html', result=result.text, chapter=chapter)

    lang = request.args.get('lang','american_english')
    session['lang'] = lang
    session['lang_code'] = lang_dict.get(lang.lower())
    print(lang)
    return render_template('train.html', chapter=chapter)

@app.route('/api/correction', methods=['POST'])
def correction():
    if request.method == 'POST':
        # json data
        data = request.get_json()
        original_text = data.get('original_text')
        spoken_text = data.get('spoken_text')
        print(f'Original Text: {original_text}')
        print(f'Spoken Text: {spoken_text}')
        result = correction_api(original_text, spoken_text)
        print(result.text)
        final_answer = result.text.replace('```html\n','').replace('```','')
        return json.dumps({'result':final_answer})
    return json.dumps({'result':'error'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

def get_user_info(user_id):
    db_session = open_db()
    user = db_session.query(User).filter_by(id=user_id).first()
    username = user.username if user else None
    email = user.email if user else None
    db_session.close()  # Close the database session after querying
    return username, email

@app.route('/profile')
def profile():
    if 'isauth' not in session or not session.get('isauth'):
        return redirect('/login')
    user_id = session.get('id')  # Use 'id' instead of 'user_id' key
    if not user_id:
        return redirect('/login')
    username, email = get_user_info(user_id)
    return render_template('profile.html', username=username, email=email)


if __name__ == "__main__":
    app.run(debug=True)
