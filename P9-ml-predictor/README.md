# P9 — Mielelezo: Spam Predictor kwa Machine Learning (mradi wa MWISHO!)

## Maelezo Mafupi (Description)
Programu inayotambua **spam vs ujumbe halisi** (SMS/WhatsApp) kwa kutumia
**scikit-learn**: TF-IDF + Naive Bayes, ikiwa na **train/test split**,
metriki (precision/recall/F1/confusion matrix) na **model iliyohifadhiwa**
(pickle). Data: `sms.csv` (mifano 74 ya Kiswahili/Kiingereza).

## Kwa nini (Business value)
- **Scam za SMS/WhatsApp ni tatizo halisi TZ** (bahati nasibu, "umeshinda",
  OTP fraud) - kila simu ya kibiashara inapaswa kupangwa
- **False positive ni ghali**: ujumbe halisi unapokataliwa = mteja
  haelewi taarifa yake (ona mfano wetu halisi hapa chini!)
- **Tunatumia OFFLINE** - data yetu, kompyuta yetu (3.3: hakuna data
  inayoenda kwa Google/OpenAI)

## Nadharia kwa maana halisi (Theory)
| Dhana | Sampuli ya maisha |
|---|---|
| **TF-IDF** | Neno "tuma" liko mara nyingi = "muhimu"; lakini liko **kila aina** = hailiongezi sana |
| **Naive Bayes** | "Ujumbe ukiwa na maneno yafuatayo, ni asilimia ngapi spam?" (kanuni ya Bayes kwa lugha) |
| **Train/Test split** | Soma mitihani = **kujifunza**; mtihani halisi = **kujithibitisha** (25% haikuonekani!) |
| **Overfitting** | Kama ulifunzwa maswali YALE YALE ya mtihani - utajibu vizuri lakini **haujui** (hivyo tunatenganisha!) |
| **Precision** | Kati ya alizoita SPAM, ni ngapi **kweli** spam? (spam 90%: 1 halisi amekataliwa) |
| **Recall** | Kati ya spam ZOTE, amzipata ngapi? |

**Mfano wetu halisi (mbegu 42, asilimia 94.7):**
- SPAM: precision 0.90 (aliita spam 10; 9 ni kweli, **1 ni halisi amekataliwa**)
- Ujumbe halisi *"Tuma kwa namba ile ile ya kawaida ya kampuni"*
  mpiliwetu uliitwa **SPAM (65%)** - ni **false positive** kweli!

## Jinsi ya kutumia (How to run)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO\P9-ml-predictor
python mielelezo.py fundisha          # funisha + onyesha metriki
python mielelezo.py angalia "Umeshinda zawadi tuma namba ya siri"
python mielelezo.py angalia "Habari ya asubuhi umefika salama"
python mielelezo.py thibitisha         # metriki za model iliyohifadhiwa
```
Au double-click `mielelezo.bat` (inaonyesha msaada).

**GUI (Tkinter):** `python mielelezo_gui.py` au `mielelezo_gui.bat`
- Tab **Tabiri**: andika ujumbe → SPAM/HAM + uwezo% (rangi nyekundu/kijani)
- Tab **Fundisha**: funisha model (thread - UI haijakwama) + metriki
- Tab **Data**: takwimu za sms.csv

**Matokeo halisi:** Usahihi **94.7%** (18 kati ya 19 sawa).

## Ethical AI (3.3 - muhimu)
1. **False positives**: ujumbe halisi unapokataliwa = hasara ya mteja -
   hivyo **precision haipaswi kuwa chini** kwenye matumizi halisi
2. **Bias ya lugha**: model yetu imefunzwa **Kiswahili/Kiingereza** tu -
   haifanyi kazi vizuri kwenye lugha nyingine (haina "ulemavu" - ni **mdhaifu**)
3. **Faragha**: SMS ni **binafsi** - usitume kwa server za nje bila ruhusa
4. **Data ndogo** (74): model hii ni **demo** - ya halisi inahitaji
   mifano **elfu/kamilioni** + kusasishwa mara kwa mara (concept drift:
   wawindaji hubadilisha maneno yao!)
5. **Si kweli 100%**: hakuna model kamili - inapaswa kuwa **msaada** wa
   mtu, si hukumu ya mwisho

## Malengo ya kiwango cha juu (Production upgrades)
1. **Data kubwa** (elfu+) + kusafisha (stopwords, stemming)
2. **LSTM/Transformer** (deep learning) au **Ollama LLM** (3.3) kulinganisha
3. **API** (Flask/FastAPI) + kuunganisha na P6 (SMS za wateja)
4. **Retraining/monitoring**: matumizi hubadilika = model ina slice old
5. **Explainability**: onyesha **maneno gani** yalisababisha hukumu (SHAP)
6. **A/B testing** kabla ya kuweka production

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1-P8
- [x] P9 — Mielelezo (hii) — **PORTFOLIO IMEKAMILIKA!**
