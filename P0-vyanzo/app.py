# WEB + DATABASE - Flask app (web + DB + jedwali la malipo)
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)


def get_conn():
    conn = sqlite3.connect('benki.db')
    conn.row_factory = sqlite3.Row
    return conn


# Hakikisha jedwali lipo kabla ya kila kitu
conn = get_conn()
conn.execute('''CREATE TABLE IF NOT EXISTS mikopo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mteja TEXT NOT NULL,
    kiasi REAL NOT NULL,
    riba REAL NOT NULL,
    miezi INTEGER NOT NULL,
    tarehe TEXT DEFAULT (date('now')))''')
conn.commit()
conn.close()

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Benki ya Mkopo - Flask</title>
    <style>
        body { font-family: Arial; background-color: #f0f4f8; margin: 40px; }
        h1 { color: #0b5394; }
        .kadi { background: white; padding: 25px; border-radius: 10px;
                border-left: 5px solid #0b5394; max-width: 750px; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input { width: 95%; padding: 8px; margin-top: 4px; border: 1px solid #ccc;
                border-radius: 5px; }
        button { background-color: #0b5394; color: white; padding: 12px 25px;
                 border: none; border-radius: 5px; cursor: pointer; margin-top: 15px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: right; }
        th { background-color: #0b5394; color: white; }
        td:first-child, th:first-child { text-align: left; }
        a { color: #0b5394; font-weight: bold; }
    </style>
</head>
<body>
    <h1>&#127974; Benki ya Mkopo (Flask + SQLite)</h1>

    <div class="kadi">
        <h3>Ingiza mkopo mpya</h3>
        <form method="post" action="/ongeza">
            <label>Mteja:</label>
            <input type="text" name="mteja" required>

            <label>Kiasi (TZS):</label>
            <input type="number" name="kiasi" required>

            <label>Riba kwa mwaka (%):</label>
            <input type="number" name="riba" required>

            <label>Muda (miezi):</label>
            <input type="number" name="miezi" required>

            <button type="submit">HIFADHI MKOPO</button>
        </form>

        <h3>Orodha ya mikopo (kutoka benki.db)</h3>
        <table>
            <tr>
                <th>#</th><th>Mteja</th><th>Kiasi</th><th>Riba%</th>
                <th>Miezi</th><th>Malipo/Mwezi</th><th>Tarehe</th><th></th>
            </tr>
            {% for m in mikopo %}
            {% set jumla = m.kiasi + m.kiasi * m.riba / 100 * (m.miezi / 12) %}
            <tr>
                <td>{{ m.id }}</td>
                <td>{{ m.mteja }}</td>
                <td>{{ "%.0f"|format(m.kiasi) }}</td>
                <td>{{ m.riba }}</td>
                <td>{{ m.miezi }}</td>
                <td><b>{{ "%.0f"|format(jumla / m.miezi) }}</b></td>
                <td>{{ m.tarehe }}</td>
                <td><a href="/jedwali/{{ m.id }}">Jedwali &raquo;</a></td>
            </tr>
            {% endfor %}
        </table>
        <p>Jumla ya mikopo: {{ mikopo|length }}</p>
    </div>
</body>
</html>
'''

JEDWALI_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Jedwali la Malipo</title>
    <style>
        body { font-family: Arial; background-color: #f0f4f8; margin: 40px; }
        h1 { color: #0b5394; }
        .kadi { background: white; padding: 25px; border-radius: 10px;
                border-left: 5px solid #0b5394; max-width: 750px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: right; }
        th { background-color: #0b5394; color: white; }
        a { color: #0b5394; font-weight: bold; }
    </style>
</head>
<body>
    <div class="kadi">
        <h1>Jedwali la Malipo - {{ m.mteja }}</h1>
        <p><b>Kiasi:</b> {{ "%.0f"|format(m.kiasi) }} TZS |
           <b>Riba:</b> {{ m.riba }}% |
           <b>Miezi:</b> {{ m.miezi }} |
           <b>Jumla ya deni:</b> {{ "%.0f"|format(jumla) }} TZS |
           <b>Malipo/mwezi:</b> {{ "%.0f"|format(kila_mwezi) }} TZS</p>
        <p><a href="/">&laquo; Rudia kwenye orodha</a></p>
        <table>
            <tr><th>Mwezi</th><th>Riba</th><th>Marejesho</th><th>Iliyolipwa</th>
                <th>Iliyobaki</th><th>Salio la deni</th></tr>
            {% for mwezi, riba_m, marejesho, iliyolipwa, iliyobaki, salio in masafu %}
            <tr>
                <td>{{ mwezi }}</td>
                <td>{{ "%.0f"|format(riba_m) }}</td>
                <td>{{ "%.0f"|format(marejesho) }}</td>
                <td>{{ "%.0f"|format(iliyolipwa) }}</td>
                <td><b>{{ "%.0f"|format(iliyobaki) }}</b></td>
                <td>{{ "%.0f"|format(salio) }}</td>
            </tr>
            {% endfor %}
        </table>
        <p><a href="/">&laquo; Rudia kwenye orodha</a></p>
    </div>
</body>
</html>
'''


@app.route('/')
def nyumbani():
    conn = get_conn()
    mikopo = conn.execute('SELECT * FROM mikopo ORDER BY id DESC').fetchall()
    conn.close()
    return render_template_string(HTML, mikopo=mikopo)


@app.route('/ongeza', methods=['POST'])
def ongeza():
    mteja = request.form['mteja']
    kiasi = float(request.form['kiasi'])
    riba = float(request.form['riba'])
    miezi = int(request.form['miezi'])

    conn = get_conn()
    conn.execute(
        'INSERT INTO mikopo (mteja, kiasi, riba, miezi) VALUES (?,?,?,?)',
        (mteja, kiasi, riba, miezi))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/jedwali/<int:id>')
def jedwali(id):
    conn = get_conn()
    m = conn.execute('SELECT * FROM mikopo WHERE id = ?', (id,)).fetchone()
    conn.close()

    if m is None:
        return 'Hakuna mkopo kama huo', 404

    jumla_riba = m['kiasi'] * m['riba'] / 100 * (m['miezi'] / 12)
    jumla = m['kiasi'] + jumla_riba
    kila_mwezi = jumla / m['miezi']
    riba_kila_mwezi = jumla_riba / m['miezi']
    marejesho = kila_mwezi - riba_kila_mwezi

    masafu = []
    salio = m['kiasi']
    for i in range(1, m['miezi'] + 1):
        salio = salio - marejesho
        if salio < 1:
            salio = 0
        iliyolipwa = kila_mwezi * i
        iliyobaki = jumla - iliyolipwa
        masafu.append((i, riba_kila_mwezi, marejesho, iliyolipwa, iliyobaki, salio))

    return render_template_string(JEDWALI_HTML, m=m, jumla=jumla,
                                  kila_mwezi=kila_mwezi, masafu=masafu)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
