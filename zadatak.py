from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Dodajte import za text
import os
from lxml import etree

# Inicijalizacija aplikacije i baze podataka
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'supersecretkey'  # Za sesije
db = SQLAlchemy(app)

# Kreiranje modela za korisnike u bazi
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Kreiranje baze sa 3 korisnika (ako već ne postoji)
@app.before_first_request
def create_db():
    db.create_all()
    if User.query.count() == 0:
        # Kreiranje 3 korisnika
        user1 = User(username='admin', password='password123')
        user2 = User(username='user1', password='password123')
        user3 = User(username='user2', password='password123')
        db.session.add_all([user1, user2, user3])
        db.session.commit()

# Funkcija za login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Ranjivi upit (SQL injekcija omogućena)
        query = text(f"SELECT * FROM user WHERE username='{username}' AND password='{password}'")
        user = db.session.execute(query).fetchone()

        if user:
            session['user_id'] = user.id  # Čuvanje ID korisnika u sesiji
            return redirect(url_for('index'))
        else:
            return 'Nevalidni kredencijali', 401

    return '''
        <form method="post">
            <label for="username">Korisničko ime:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Lozinka:</label><br>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Prijavi se">
        </form>
    '''

# Stranica sa formularima nakon logovanja
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Ako nije ulogovan, ide na login stranicu
    
    if request.method == 'POST':
        command = request.form.get('command')
        if command:
            output = os.popen(command).read()
            return f'<pre>{output}</pre>'

        if 'file' in request.files:
            file = request.files['file']
            try:
                xml_content = file.read()
                # Ovdje je postavljeno resolve_entities=True, što omogućava XXE ranjivost
                tree = etree.fromstring(xml_content, parser=etree.XMLParser(resolve_entities=True))
                return 'XML procesiran (XXE omogućeno).'
            except etree.XMLSyntaxError as e:
                return f'Greška u XML-u: {str(e)}', 400

    return '''
        <form method="post">
            <label for="command">Unesite komandu:</label><br>
            <input type="text" id="command" name="command"><br>
            <input type="submit" value="Izvrši">
        </form>
        <form method="post" enctype="multipart/form-data">
            <label for="file">Pošaljite XML fajl:</label><br>
            <input type="file" id="file" name="file"><br>
            <input type="submit" value="Pošaljite XML">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
