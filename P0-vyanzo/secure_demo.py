# PRACTICE 2 - Dictionary attack ndogo + Encryption (Fernet)
import hashlib
from cryptography.fernet import Fernet

# ============ SEHEMU 1: DICTIONARY ATTACK ============
print('=== DICTIONARY ATTACK ===')

# Password zinazotumika duniani (orodha fupi ya mfano)
dictionary = [
    '123456', 'password', '123456789', 'qwerty', 'abc123',
    'password123', 'letmein', 'admin', 'welcome', 'monkey',
    'iloveyou', 'Asha2026', 'Tz2026', 'football', 'master','Edward'
]

# Hash halisi ya password iliyovuja (mfano: ya 'password123')
hash_ya_mwizi = 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'

imevunjwa = False
for password in dictionary:
    jaribio = hashlib.sha256(password.encode()).hexdigest()
    if jaribio == hash_ya_mwizi:
        print('VUNJIWA! Password ni:', password)
        imevunjwa = True
        break

if not imevunjwa:
    print('Haijavunjwa kwenye orodha hii')

# Jaribu na password imara - itavunjika?
password_imara = 'K!9mZ#2vQ$7xLp4R'
print('\nInajaribu password imara:', password_imara)
jaribio = hashlib.sha256(password_imara.encode()).hexdigest()
imevunjwa = False
for password in dictionary:
    if hashlib.sha256(password.encode()).hexdigest() == jaribio:
        imevunjwa = True
        break
print('Imevunjika?' , imevunjwa, '->', 'HAPANA! Hakuna kwenye orodha' if not imevunjwa else 'NDIYO')

# ============ SEHEMU 2: ENCRYPTION (FERNET) ============
print('\n=== ENCRYPTION (kufunga na kufungua) ===')

# 1. Tengeneza ufunguo (siri sana - huhifadhiwa kwa usalama)
ufunguo = Fernet.generate_key()
print('Ufunguo:', ufunguo[:30], '...')

cipher = Fernet(ufunguo)

# 2. Funga ujumbe
ujumbe_wa_asili = 'Salio la akaunti yako ni TZS 5,000,000'
umefungwa = cipher.encrypt(ujumbe_wa_asili.encode())
print('\nAsili  :', ujumbe_wa_asili)
print('Umefungwa:', umefungwa[:60], '...')

# 3. fungua tena (kwa ufunguo ule ule)
umefunguliwa = cipher.decrypt(umefungwa).decode()
print('Umerudishwa:', umefunguliwa)
print('Umefanana?', umefunguliwa == ujumbe_wa_asili)

# 4. Jaribu kufungua BILA ufunguo sawa
print('\n--- Jaribio la kufungua bila ufunguo sahihi ---')
try:
    cipher_mbovu = Fernet(Fernet.generate_key())
    cipher_mbovu.decrypt(umefungwa)
except Exception:
    print('IMESHINDWA kufungua! (InvalidToken) - hivyo ndivyo mwizi anavyoshindwa')
