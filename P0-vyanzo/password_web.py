# PROJECT #3 (Web version) - PASSWORD TOOL kwenye browser (Flask)
from flask import Flask, request, render_template_string
import hashlib
import secrets
import string

app = Flask(__name__)

DICT_DHAIFU = [
    '123456', 'password', '123456789', 'qwerty', 'abc123',
    'password123', 'letmein', 'admin', 'welcome', 'monkey',
    'iloveyou', 'football', 'master', 'asha2026', 'tz2026'
]


def hash_password(password, salt=''):
    return hashlib.sha256((salt + password).encode()).hexdigest()


def tengeneza(urefu=16):
    herufi = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(herufi) for _ in range(urefu))


def tathmini(password):
    if password.lower() in DICT_DHAIFU:
        return 0, '[!!] Iko kwenye orodha ya watu duniani!'
    alama = 0
    onyo = ''
    if len(password) >= 12:
        alama += 1
    else:
        onyo = '[!!] Fupi sana (chini ya herufi 12)'
    if any(c.isupper() for c in password) and any(c.islower() for c in password):
        alama += 1
    if any(c.isdigit() for c in password):
        alama += 1
    if any(not c.isalnum() for c in password):
        alama += 1
    maoni = ['HAIWEZI', 'Dhaifu', 'Wastani', 'Nzuri', 'IMARA kabisa']
    return alama, f'Alama: {alama}/4 -> {maoni[alama]} {onyo}'


HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Password Tool</title>
    <style>
        body { font-family: Arial; background-color: #f0f4f8; margin: 40px; }
        h1 { color: #0b5394; }
        .kadi { background: white; padding: 20px; border-radius: 10px;
                border-left: 5px solid #0b5394; max-width: 650px;
                margin-bottom: 20px; }
        label { display: block; margin-top: 8px; font-weight: bold; }
        input[type=text], input[type=password] { width: 95%; padding: 8px;
                margin-top: 4px; border: 1px solid #ccc; border-radius: 5px; }
        button { background-color: #0b5394; color: white; padding: 10px 20px;
                 border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; }
        .matokeo { background: #e8f5e9; padding: 15px; border-radius: 8px;
                   border-left: 5px solid #2e7d32; word-wrap: break-word; }
        .mbaya { background: #fdecea; border-left-color: #b71c1c; }
        .kidogo { font-size: 13px; color: #555; }
    </style>
</head>
<body>
    <h1>&#128274; Password Tool (Web)</h1>

    {% if result %}
    <div class="kadi matokeo {{ matabaya }}">{{ result|safe }}</div>
    {% endif %}

    <div class="kadi">
        <h3>1. Hash password (na salt)</h3>
        <form method="post">
            <input type="hidden" name="kitendo" value="hash">
            <label>Password:</label>
            <input type="password" name="password" required>
            <label><input type="checkbox" name="salt"> Tumia salt ya kipekee</label>
            <button type="submit">HASHER</button>
        </form>
    </div>

    <div class="kadi">
        <h3>2. Thibitisha (login)</h3>
        <form method="post">
            <input type="hidden" name="kitendo" value="thibitisha">
            <label>Password ya kujaribu:</label>
            <input type="password" name="password" required>
            <label>Hash iliyohifadhiwa:</label>
            <input type="text" name="hash" required>
            <label>Salt (kama ipo):</label>
            <input type="text" name="salt">
            <button type="submit">THIBITISHA</button>
        </form>
    </div>

    <div class="kadi">
        <h3>3. Tathmini nguvu</h3>
        <form method="post">
            <input type="hidden" name="kitendo" value="tathmini">
            <label>Password:</label>
            <input type="text" name="password" required>
            <button type="submit">TATHMINI</button>
        </form>
    </div>

    <div class="kadi">
        <h3>4. Tengeneza password imara</h3>
        <form method="post">
            <input type="hidden" name="kitendo" value="tengeneza">
            <button type="submit">TENGENEZA</button>
        </form>
        <p class="kidogo">Urefu: herufi 16 (herufi kubwa/ndogo + nambari + symbols)</p>
    </div>
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def nyumbani():
    result = ''
    matabaya = ''
    if request.method == 'POST':
        kitendo = request.form.get('kitendo')

        if kitendo == 'hash':
            password = request.form['password']
            salt = secrets.token_hex(8) if request.form.get('salt') else ''
            h = hash_password(password, salt)
            result = (f'<b>Salt:</b> {salt or "(hakuna)"}<br>'
                      f'<b>Hash (SHA256):</b> {h}')

        elif kitendo == 'thibitisha':
            password = request.form['password']
            hash_ = request.form['hash']
            salt = request.form['salt']
            if hash_password(password, salt) == hash_:
                result = '&#9989; PASSWORD SAHIHI - umeingia!'
            else:
                result = '&#10060; HASH HAIJAFANANA - password si sahihi'
                matabaya = 'mbaya'

        elif kitendo == 'tathmini':
            password = request.form['password']
            alama, ujumbe = tathmini(password)
            result = ujumbe
            if alama <= 1:
                matabaya = 'mbaya'

        elif kitendo == 'tengeneza':
            p = tengeneza()
            result = (f'<b>Password imara:</b> {p}<br>'
                      f'<b>Hash yake:</b> {hash_password(p)}')

    return render_template_string(HTML, result=result, matabaya=matabaya)


if __name__ == '__main__':
    app.run(debug=True)
