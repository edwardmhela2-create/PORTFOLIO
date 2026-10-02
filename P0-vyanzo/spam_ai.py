# PRACTICE 3 - AI YA OFFLINE: Spam detector wetu wenyewe (bila internet)
# Kanuni: neno linaonekana mara ngapi kwenye spam vs halali?

mifano = [
    ("Umeshinda bonus ya Tsh 5,000,000 tuma kodi ya siri", "spam"),
    ("Karibu tukupatie mkopo wa haraka bila dhamana haraka", "spam"),
    ("Click link hii sasa upate zawadi ya gari", "spam"),
    ("Tsh 2,000,000 zimeingia akaunti yako tuma namba ya siri", "spam"),
    ("Msichana akupigie usiku huu click hapa", "spam"),
    ("Boss nimepokea malipo ya kesho nitawasiliana nawe", "spam"),
    ("Wewe ni mshindi wa bahati nasibu tuma PIN ya simu yako", "spam"),
    ("Mkopo wa haraka bila dhamana sasa tuma kitambulisho", "spam"),
    ("Nimekuona umepata bonus tuma namba ya siri haraka", "spam"),
    ("Tuma Tsh 10,000 upate zawadi ya gari haraka sasa", "spam"),
    ("Habari za asubuhi nimefika salama nikupigie kesho", "ham"),
    ("Kikao cha kesho saa tatu ofisini tafadhali usichelewe", "ham"),
    ("Nimekuona umepata bonanza ya kazi nzuri sana", "ham"),
    ("Tsh 5,000 nimekutumia kwa basi kesho asubuhi", "ham"),
    ("Mama yako anataka uwapigie usiku huu wa jamani", "ham"),
    ("Nimepokea malipo ya mkopo tuma taarifa zako", "ham"),
    ("Safari ya kesho tutaondoka saa kumi asubuhi", "ham"),
    ("Baba yako amefika salama Mwanza leo", "ham"),
    ("Nimekuona umepata gari jipya hongera sana", "ham"),
    ("Tafadhali nisaidie kubeba mizigo kesho asubuhi", "ham"),
    ("Nimepokea taarifa zako nitasema na meneja wangu", "ham"),
    ("Tuma kodi yako kesho nakupelelea mizigo", "ham"),
    ("Habari za mapema nimefika salama bila shida", "ham"),
    ("Nitaleta taarifa za mkopo kesho ofisini", "ham"), 
    ("Nitakupigia kesho baada ya kikao cha ofisi", "ham"),
]

# ===== HATUA 1: FUNDSHA =====
# hesabu: kila neno limeonekana mara ngapi kwenye kila aina?
masomo = {"spam": {}, "ham": {}}
idadi = {"spam": 0, "ham": 0}

for ujumbe, aina in mifano:
    idadi[aina] += 1
    for neno in ujumbe.lower().split():
        masomo[aina][neno] = masomo[aina].get(neno, 0) + 1

print('=== NILICHOFUNZWA ===')
print('Mifano ya spam:', idadi['spam'], '| ya halali:', idadi['ham'])
neno_beo = "tuma"
print('Neno "%s" limeonekana: spam %d mara, halali %d mara'
      % (neno_beo, masomo['spam'].get(neno_beo, 0),
         masomo['ham'].get(neno_beo, 0)))

# ===== HATUA 2: TABIRI =====
def tabiri(ujumbe):
    alama = {"spam": 1, "ham": 1}   # 1 = msingi usio na neno lolote
    for neno in ujumbe.lower().split():
        for aina in alama:
            alama[aina] += masomo[aina].get(neno, 0)
    if alama['spam'] > alama['ham']:
        return 'spam', alama
    return 'ham', alama

# ===== HATUA 3: MTIHANI =====
print('\n=== MTIHANI (mifano ambayo HAIKUWA FUNZO) ===')
majaribio = [
    "Tuma namba yako ya siri upate bonus ya gari",
    "Nitakupigia kesho asubuhi baada ya kikao",
    "Tsh 50,000 zimefika akaunti tuma taarifa zako",
    "Click hapa sasa upate zawadi ya haraka",
]

kwa_jpozitiwa = 0
majibu_halisi = ['spam', 'ham', 'ham', 'spam']

for i, ujumbe in enumerate(majaribio):
    aina, alama = tabiri(ujumbe)
    sawa = 'SAWA' if aina == majibu_halisi[i] else 'MAKOSA'
    if aina == majibu_halisi[i]:
        kwa_jpozitiwa += 1
    print('"%s"' % ujumbe)
    print('  ->', aina.upper(), '| alama: spam=%d ham=%d | %s'
          % (alama['spam'], alama['ham'], sawa))

print('\nAlama: %d kati ya %d = %d%%'
      % (kwa_jpozitiwa, len(majaribio),
         100 * kwa_jpozitiwa // len(majaribio)))

# ===== HATUA 4: KARIBI NOGODA =====
print('\n=== UJUZI: neno ambalo limeonekana kwenye MIBILI ===')
kwa_wote = []
for neno in masomo['spam']:
    if neno in masomo['ham']:
        kwa_wote.append(neno)
print('Maneno yanayoonekana MIBILI:', kwa_wote)
print('Haya ndiyo haina nguvu ya kutenganisha - neno la SPAM halisi')
print('linaloonekana spam pekee:', [n for n in masomo['spam']
                                     if n not in masomo['ham']])
