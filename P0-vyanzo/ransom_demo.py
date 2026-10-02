# PRACTICE 2 HALISI - Kuona encryption + ransomware kikamilifu
# KAZI: inafanya kazi kwenye folder moja tu: 'jaribio'
import os
from cryptography.fernet import Fernet

FOLDER = 'jaribio'

# ============ HATUA 1: Tengeneza folder na mafaili halisi ============
os.makedirs(FOLDER, exist_ok=True)
if not os.listdir(FOLDER):
    with open(os.path.join(FOLDER, 'ripoti.txt'), 'w', encoding='utf-8') as f:
        f.write('RIPOTI YA KAZI\nMteja: Asha\nSalio: TZS 5,000,000\nHii ni data muhimu sana.')
    with open(os.path.join(FOLDER, 'namba_zangu.txt'), 'w', encoding='utf-8') as f:
        f.write('Namba ya siri: 11223344\nWeka hapa data halisi unayoitunza.')
print('1. Folder imetengenezwa:', FOLDER)
print('   Mafaili:', os.listdir(FOLDER))

# ============ HATUA 2: Funga mafaili YOTE ============
ufunguo = Fernet.generate_key()
with open('funguo.key', 'wb') as f:
    f.write(ufunguo)
cipher = Fernet(ufunguo)

print('\n2. NAFUNGA mafaili...')
for jina in os.listdir(FOLDER):
    njia = os.path.join(FOLDER, jina)
    with open(njia, 'rb') as f:
        data = f.read()
    with open(njia + '.ufungwa', 'wb') as f:
        f.write(cipher.encrypt(data))
    os.remove(njia)
    print('   UMEFUNGWA:', jina, '->', jina + '.ufungwa')

print('\n   >>> Jaribu sasa kufungua ripoti.txt kwenye Notepad... HAIPO!')
print('   >>> Badala yake kuna .ufungwa - ukifungua utaona herufi zisizo na maana')

input('\n   [Bonyeza ENTER kuona jinsi ya kufungua upya...]')

# ============ HATUA 3: Fungua tena (kwa ufunguo) ============
print('\n3. NAFUNGUA tena kwa ufunguo...')
with open('funguo.key', 'rb') as f:
    cipher = Fernet(f.read())

for jina in os.listdir(FOLDER):
    if jina.endswith('.ufungwa'):
        njia = os.path.join(FOLDER, jina)
        with open(njia, 'rb') as f:
            asili = cipher.decrypt(f.read())
        jina_halisi = jina[:-8]
        with open(os.path.join(FOLDER, jina_halisi), 'wb') as f:
            f.write(asili)
        os.remove(njia)
        print('   UMEFUNGULIWA:', jina_halisi)

print('\n   Mafaili yote yamerudi halisi:', os.listdir(FOLDER))
print('\n=== KILICHOTOKEA ===')
print('- Data ilifungwa kwa UFUNGUO (encryption) - si password ya kukumbuka')
print('- Bila funguo.key: HAUWEZI kufungua HATA kwa miaka')
print('- RANSOMWARE halisi: hii hii, ila mwizi HAKUPI funguo - anaulipa BTC')
print('- BITLOCKER/WhatsApp: hii hii, ila funguo ni yako/salama')
