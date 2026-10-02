# Wrote mkopo.py
# Mkopo Calculator - Project #1 (Full: ulinzi + jedwali sahihi la malipo)
print('=== MAKADIRIO YA MKOPO ===')

# --- MUONGO: kurudia hadi kupata data sahihi ---
while True:
    try:
        kiasi = float(input('Kiasi cha mkopo (TZS): '))
        riba = float(input('Riba kwa mwaka (%): '))
        miezi = int(input('Muda wa malipo (miezi): '))
        if kiasi <= 0 or miezi <= 0:
            print('Hitilafu: Kiasi na miezi lazima ziwe zaidi ya 0 — jaribu tena')
            continue
        break
    except ValueError:
        print('Hiyo si namba sahihi — jaribu tena')

# --- HESABU (data daima ni sahihi hapa) ---
jumla_ya_riba = kiasi * riba / 100 * (miezi / 12)
jumla = kiasi + jumla_ya_riba
kila_mwezi = jumla / miezi

print('--- MATOKEO ---')
print('Riba ya jumla :', format(jumla_ya_riba, ',.0f'))
print('Jumla ya deni :', format(jumla, ',.0f'))
print('Malipo/mwezi  :', format(kila_mwezi, ',.0f'))

# --- JEDWALI LA MALIPO (flat riba - hesabu moja tu) ---
print('--- JEDWALI LA MALIPO ---')
riba_kila_mwezi = jumla_ya_riba / miezi
marejesho = kila_mwezi - riba_kila_mwezi
salio = kiasi
mwezi = 1

while salio > 1:
    salio = salio - marejesho
    if salio < 1:
        salio = 0
    print('Mwezi', str(mwezi).rjust(2),
          '| marejesho:', format(marejesho, ',.0f').rjust(9),
          '| salio:', format(salio, ',.0f').rjust(9))
    mwezi = mwezi + 1

print('Deni limekamilika baada ya', mwezi - 1, 'miezi')
