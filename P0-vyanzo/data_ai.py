# PRACTICE 1 - DATA ANALYSIS kwa Pandas (data ya mikopo 200)
import pandas as pd
import numpy as np

np.random.seed(42)   # ili data izidi sawa kila ukirudia

# ============ 1. Tengeneza data ya mfano (kama DB halisi) ============
n = 200
mikopo = pd.DataFrame({
    'mteja': ['Mtaji', 'Neema', 'Baraka', 'Zawadi', 'Tumaini', 'Furaha',
              'Juma', 'Asha', 'Rehema', 'Kibaha'] * 20,
    'mkoa': np.random.choice(['Dar', 'Mwanza', 'Arusha', 'Dodoma'], n),
    'kiasi': np.random.choice([250000, 500000, 1000000, 1500000, 2000000], n,
                              p=[0.3, 0.25, 0.2, 0.15, 0.1]),
    'riba': np.random.choice([10, 12, 15, 18], n),
    'miezi': np.random.choice([6, 12, 24, 36], n),
    'kulipwa': np.random.choice([True, False], n, p=[0.75, 0.25]),
})

print('=== 1. MWONEKANO WA DATA (kama Excel) ===')
print(mikopo.head())

print('\n=== 2. TAARIFA ZA JUMLA (describe) ===')
print(mikopo.describe())

print('\n=== 3. WASTANI WA KILA SULUHISHO ===')
print('Wastani wa kiasi   :', format(mikopo['kiasi'].mean(), ',.0f'))
print('Kiasi kikubwa zaidi:', format(mikopo['kiasi'].max(), ',.0f'))
print('Kiasi kidogo zaidi :', format(mikopo['kiasi'].min(), ',.0f'))

print('\n=== 4. IDADI KWA MKOA (groupby) ===')
print(mikopo.groupby('mkoa').agg(
    idadi=('kiasi', 'count'),
    wastani_wa_kiasi=('kiasi', 'mean')
).round(0))

print('\n=== 5. NI MKOA GANI UNA DENI NINI? (kulipwa rates) ===')
kulipwa_kwa_mkao = mikopo.groupby('mkoa')['kulipwa'].mean() * 100
print(kulipwa_kwa_mkao.round(1).sort_values(ascending=False))

print('\n=== 6. MICRO-INSIGHT: muda na kiasi ===')
print(mikopo.groupby('miezi')['kiasi'].mean().apply(lambda x: format(x, ',.0f')))

print('\n=== 7. CHUJA: mikopo zaidi ya milioni 1 ===')
mikubwa = mikopo[mikopo['kiasi'] > 1000000]
print('Idadi:', len(mikubwa), 'kati ya', len(mikopo))
print(mikubwa.head())
