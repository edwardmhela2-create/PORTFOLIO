# PRACTICE 3 (OFFLINE) - PORT SCANNER (ethical hacking - hatua ya SCAN)
# Inachunguza laptop YAKO pekee (127.0.0.1) - si za mtu mwingine
import socket
from concurrent.futures import ThreadPoolExecutor

# Porti muhimu + huduma zake (haya ndiyo "milango" tunayochunguza)
PORTI_ZINAZOTAJIKA = {
    21: 'FTP', 22: 'SSH', 23: 'Telena', 25: 'SMTP', 53: 'DNS',
    80: 'HTTP (tovuti)', 110: 'POP3', 135: 'RPC (Windows)',
    139: 'NetBIOS', 143: 'IMAP', 443: 'HTTPS (tovuti salama)',
    445: 'SMB (shiriki mafaili)', 3306: 'MySQL', 3389: 'RDP (Windows remote)',
    5432: 'PostgreSQL', 5900: 'VNC', 8080: 'HTTP ya siri (proxy)',
    27015: 'MongoDB',
}


def jaribu_porti(ip, porti):
    """Jaribu kuunganisha porti moja - rudisha True kama iko wazi"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)          # subiri sekunde 0.3 tu kila jaribio
        mafanikio = s.connect_ex((ip, porti)) == 0
        s.close()
        return mafanikio
    except Exception:
        return False


print('=== PORT SCANNER (laptop yako pekee) ===')
ip = input('Target (bonyeza ENTER kwa laptop yako): ').strip() or '127.0.0.1'
print('Inachunguza porti', len(PORTI_ZINAZOTAJIKA), 'za kawaida...')

zilizofunguliwa = []
with ThreadPoolExecutor(max_workers=20) as executor:
    majibu = executor.map(lambda p: jaribu_porti(ip, p), PORTI_ZINAZOTAJIKA.keys())
    for porti, wazi in zip(PORTI_ZINAZOTAJIKA.keys(), majibu):
        if wazi:
            zilizofunguliwa.append(porti)

print('\n=== MATOKEO ===')
if not zilizofunguliwa:
    print('Hakuna porti iliyopatikana wazi (rare - firewall imeziba kila kitu)')
for porti in zilizofunguliwa:
    huduma = PORTI_ZINAZOTAJIKA.get(porti, 'haijulikani')
    print(f'  [WAZI] porti {porti:<6} - {huduma}')

print('\nUshauri wa usalama:')
for porti in zilizofunguliwa:
    if porti in (139, 445, 3389, 23):
        print(f'  [!] Porti {porti} ina hatari kubwa kwenye WiFi ya umma - funga kama huitumii')
