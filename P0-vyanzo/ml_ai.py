# PRACTICE 2 - ML WA KWANZA: TABIRI NANI ATALIPA
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

np.random.seed(42)
n = 200

kiasi = np.random.choice([250000, 500000, 1000000, 1500000, 2000000], n,
                         p=[0.3, 0.25, 0.2, 0.15, 0.1])
riba = np.random.choice([10, 12, 15, 18], n)
miezi = np.random.choice([6, 12, 24, 36], n)
mkoa = np.random.choice(['Dar', 'Mwanza', 'Arusha', 'Dodoma'], n)

# label inategemea kiasi (kuna mfumo halisi ndani ya data)
uwezekano = np.where(kiasi <= 500000, 0.9,
             np.where(kiasi <= 1000000, 0.7, 0.55))
kulipwa = np.random.rand(n) < uwezekano

df = pd.DataFrame({'kiasi': kiasi, 'riba': riba, 'miezi': miezi,
                   'mkoa': mkoa, 'kulipwa': kulipwa})

print('=== DATA ===')
print(df.head())

# X = sifa (features), y = jibu (label)
X = pd.get_dummies(df.drop('kulipwa', axis=1), columns=['mkoa'])
y = df['kulipwa']
print('\nSifa zinazotumika:', list(X.columns))

# 80% kufundisha / 20% kupima
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print('Kufundisha:', len(X_train), '| Kupima:', len(X_test))

# fundisha model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# pima na data model HAIKUONA
pred = model.predict(X_test)
print('\n=== MATOKEO ===')
print('Accuracy: %', round(accuracy_score(y_test, pred) * 100, 1))
print('Confusion matrix:')
print(confusion_matrix(y_test, pred))

# ni sifa gani muhimu zaidi?
umuhimu = pd.Series(model.feature_importances_,
                    index=X.columns).sort_values(ascending=False)
print('\nUmuhimu wa sifa (%):')
print((umuhimu * 100).round(1))

# tabiri mteja mpya: kiasi 300,000 | riba 12 | miezi 6 | Dar
mteja_mpya = pd.DataFrame([{
    'kiasi': 300000, 'riba': 12, 'miezi': 6,
    'mkoa_Dar': 1, 'mkoa_Mwanza': 0,
    'mkoa_Arusha': 0, 'mkoa_Dodoma': 0
}]).reindex(columns=X.columns, fill_value=0)

jibu = model.predict(mteja_mpya)[0]
print('\n=== TABIRI MTEJA MPYA ===')
print('Kiasi 300,000 | 6 miezi | Dar es Salaam')
print('Jibu la model:', 'ATALIPA' if jibu else 'HAWATOLIPA')
