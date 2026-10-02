# DATABASE YA BENKI - Somo la SQL (SQLite kwa Python)
import sqlite3

# 1. Unganisha (au tengeneza) database - inaonekana kama benki.db
conn = sqlite3.connect('benki.db')
c = conn.cursor()

# 2. Tengeneza jedwali la mikopo (mara moja tu)
c.execute('''
    CREATE TABLE IF NOT EXISTS mikopo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mteja TEXT NOT NULL,
        kiasi REAL NOT NULL,
        riba REAL NOT NULL,
        miezi INTEGER NOT NULL,
        tarehe TEXT DEFAULT (date('now'))
    )
''')

# 3. Hakikisha jedwali halijajaa - tuingize data ya mfano mara moja tu
c.execute('SELECT COUNT(*) FROM mikopo')
if c.fetchone()[0] == 0:
    sample = [
        ('Asha',   1000000, 15, 24),
        ('Juma',    500000, 12, 12),
        ('Neema',  2000000, 18, 36),
        ('Baraka',  250000, 10, 6),
        ('Zawadi', 1500000, 15, 24),
    ]
    c.executemany('INSERT INTO mikopo (mteja, kiasi, riba, miezi) VALUES (?,?,?,?)', sample)
    conn.commit()
    print('Data ya mfano imehifadhiwa\n')

# --- MASWALI YA SQL (queries) ---

print('=== 1. ONYESHA MIKOPO YOTE ===')
c.execute('SELECT * FROM mikopo')
for row in c.fetchall():
    print(row)

print('\n=== 2. MIKOPO ZAIDI YA 500,000 ===')
c.execute('SELECT mteja, kiasi FROM mikopo WHERE kiasi > 500000')
for row in c.fetchall():
    print(row)

print('\n=== 3. JUMLA YA MIKOPO YOTE (SUM) ===')
c.execute('SELECT SUM(kiasi), COUNT(*), AVG(kiasi) FROM mikopo')
jumla, idadi, wastani = c.fetchone()
print('Jumla ya mikopo :', format(jumla, ',.0f'))
print('Idadi ya mikopo :', idadi)
print('Wastani wa mkopo:', format(wastani, ',.0f'))

print('\n=== 4. PANGA KWA UKUBWA (DESC) ===')
c.execute('SELECT mteja, kiasi FROM mikopo ORDER BY kiasi DESC')
for row in c.fetchall():
    print(row)

print('\n=== 5. SASISHA - Baraka aliongeza mkopo ===')
c.execute("UPDATE mikopo SET kiasi = 300000 WHERE mteja = 'Baraka'")
conn.commit()
c.execute("SELECT mteja, kiasi FROM mikopo WHERE mteja = 'Baraka'")
print('Mara baada ya kusasisha:', c.fetchone())

print('\n=== 6. ONDOA - Neema amelipa mkopo wake ===')
c.execute("DELETE FROM mikopo WHERE mteja = 'Neema'")
conn.commit()
c.execute('SELECT COUNT(*) FROM mikopo')
print('Mikopo iliyobaki:', c.fetchone()[0], 'mteja')

print('\n=== SWALI 1: mikopo ya miezi 24 ===')
c.execute("SELECT mteja, kiasi FROM mikopo WHERE miezi = 24")
for row in c.fetchall():
    print(row)

print('\n=== SWALI 2: riba ya zaidi ya 13% ===')
c.execute("SELECT mteja, kiasi FROM mikopo WHERE riba > 13")
for row in c.fetchall():
    print(row)

print('\n=== SWALI 3: kubwa NA mrefu ===')
c.execute("SELECT mteja, kiasi, miezi FROM mikopo WHERE kiasi > 500000 AND miezi > 12")
for row in c.fetchall():
    print(row)

print('\n=== SWALI 4: Asha AU Baraka ===')
c.execute("SELECT mteja, kiasi FROM mikopo WHERE mteja = 'Asha' OR mteja = 'Baraka'")
for row in c.fetchall():
    print(row)

print('\n=== SWALI 5: mteja mpya ===')
c.execute("INSERT INTO mikopo (mteja, kiasi, riba, miezi) VALUES ('Tumaini', 750000, 14, 18)")
conn.commit()
c.execute("SELECT * FROM mikopo WHERE mteja = 'Tumaini'")
print('Ameingia:', c.fetchone())

print('\n=== SWALI 6: mikopo kwa kila muda ===')
c.execute("SELECT miezi, COUNT(*) FROM mikopo GROUP BY miezi")
for row in c.fetchall():
    print(row)


conn.close()
print('\nDatabase imefungwa')
