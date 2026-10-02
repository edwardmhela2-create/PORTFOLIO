# PROJECT #3 - PASSWORD TOOL
# 1. Hash + salt  2. Thibitisha (login)  3. Tathmini  4. Tengeneza
import hashlib
import secrets
import string

# Password dhaifu zinazotumika duniani (orodha fupi ya mfano)
DICT_DHAIFU = [
    '123456', 'password', '123456789', 'qwerty', 'abc123',
    'password123', 'letmein', 'admin', 'welcome', 'monkey',
    'iloveyou', 'football', 'master', 'asha2026', 'tz2026'
]


def hash_password(password, salt=''):
    """Rudisha hash ya password (pamoja na salt ikiwa ipo)"""
    return hashlib.sha256((salt + password).encode()).hexdigest()


def tathmini(password):
    """Rudisha alama ya nguvu (0-4)"""
    alama = 0
    maswali = []
    if len(password) >= 12:
        alama += 1
    if any(c.isupper() for c in password) and any(c.islower() for c in password):
        alama += 1
    if any(c.isdigit() for c in password):
        alama += 1
    if any(not c.isalnum() for c in password):
        alama += 1

    if password.lower() in DICT_DHAIFU:
        print('  [!!] Iko kwenye orodha ya watu - HAIWEZI kutumika!')
        return 0
    if len(password) < 8:
        print('  [!!] Fupi sana (chini ya herufi 8)')

    return alama


def tengeneza(urefu=16):
    """Tengeneza password imara kwa kutumia secrets (si random ya kawaida)"""
    herufi = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(herufi) for _ in range(urefu))


# ============ MENU (while loop!) ============
print('=== PASSWORD TOOL ===')
chaguo = ''
while chaguo != '5':
    print('''
1. Hash password (na salt)
2. Thibitisha password dhidi ya hash (login)
3. Tathmini nguvu ya password
4. Tengeneza password imara
5. Toka''')
    chaguo = input('Chagua (1-5): ')

    if chaguo == '1':
        password = input('Weka password: ')
        tumia_salt = input('Tumia salt? (ndiyo/hapana): ').lower() == 'ndiyo'
        salt = secrets.token_hex(8) if tumia_salt else ''
        h = hash_password(password, salt)
        print('Salt  :', salt if salt else '(hakuna)')
        print('Hash  :', h)

    elif chaguo == '2':
        password = input('Weka password: ')
        hash_iliyohifadhiwa = input('Weka hash ya kulinganisha: ')
        salt_iliyohifadhiwa = input('Weka salt (au tupu): ')
        if hash_password(password, salt_iliyohifadhiwa) == hash_iliyohifadhiwa:
            print('  [OK] PASSWORD SAHIHI - umeingia!')
        else:
            print('  [X]  HASH HAIJAFANANA - password si sahihi')

    elif chaguo == '3':
        password = input('Weka password: ')
        alama = tathmini(password)
        maoni = ['HAIWEZI', 'Dhaifu', 'Wastani', 'Nzuri', 'IMARA kabisa']
        print('  Alama:', alama, '/4 ->', maoni[alama])

    elif chaguo == '4':
        p = tengeneza()
        print('Password imara:', p)
        print('Hash yake     :', hash_password(p))

    elif chaguo == '5':
        print('Kwaheri!')
    elif chaguo != '':
        print('Chaguo lisilojulikana')
