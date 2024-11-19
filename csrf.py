from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Simulacija korisničkog sistema
users = {
    'user1': {'email': 'user1@example.com', 'password': 'password123'}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Ovo je namerno ranjiva linija koda
        new_password = request.form.get('password')
        if new_password:
            # Promena lozinke
            users['user1']['password'] = new_password
            return f'Lozinka je promenjena na: {new_password}'
        else:
            return 'Greška pri promeni lozinke', 400

            
        # Ranjiva linija sa CSRF tokenom
        csrf_token = request.form.get('csrf_token')
        new_password = request.form.get('password')

        # OVDE je CSRF ranjivost - token nije vezan za sesiju korisnika!
        # Napadači mogu lako preuzeti i iskoristiti ovaj token.
        if csrf_token in csrf_tokens:  # Ovo je ranjivost!
            current_user = 'user1'  # Pretpostavljamo da je korisnik uvek 'user1'
            if current_user in users and new_password:
                users[current_user]['password'] = new_password
                return f'Lozinka je promenjena na: {new_password}'
            else:
                return 'Greška pri promeni lozinke', 400
        else:
            return 'Nevalidan CSRF token', 400

    # Generiši CSRF token i čuvaj ga u globalnoj promenljivoj (ne vezujemo za sesiju!)
    csrf_token = secrets.token_hex(16)
    csrf_tokens[csrf_token] = True  # Čuvanje tokena u globalnoj promenljivoj

    return '''
        <form method="post">
            <label for="password">Nova lozinka:</label><br>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Spremi promene">
        </form>

                <form method="post">
            <label for="password">Nova lozinka:</label><br>
            <input type="password" id="password" name="password"><br>
            <input type="hidden" name="csrf_token" value="''' + csrf_token + '''"><br>
            <input type="submit" value="Spremi promene">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)