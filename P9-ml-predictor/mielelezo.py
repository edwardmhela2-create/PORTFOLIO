import argparse
import os
import pickle
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

MJI = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(MJI, "sms.csv")
MODEL = os.path.join(MJI, "model.pkl")
MBEGU = 42


def pakua_data(njia=None):
    if njia is None:
        njia = DATA
    ujumbe, lebo = [], []
    with open(njia, encoding="utf-8") as f:
        kwa = f.readline()
        if "ujumbe" not in kwa or "label" not in kwa:
            raise ValueError("CSV hauna safu za kichwa: ujumbe,label")
        for mstari in f:
            mstari = mstari.strip()
            if not mstari:
                continue
            sehemu = mstari.rsplit(",", 1)
            if len(sehemu) != 2:
                raise ValueError("Mstari mbovu: %s" % mstari)
            u, l = sehemu[0].strip().strip('"'), sehemu[1].strip()
            if not u or l not in ("spam", "ham"):
                raise ValueError("Data mbovu: %s" % mstari)
            ujumbe.append(u)
            lebo.append(l)
    if len(ujumbe) < 20:
        raise ValueError("Data ni ndogo mno (angalau mifano 20)")
    return ujumbe, lebo


def fundisha(njia=None, model_njia=None, mbegu=MBEGU):
    if model_njia is None:
        model_njia = MODEL
    X, y = pakua_data(njia)
    X_mafunzo, X_test, y_mafunzo, y_test = train_test_split(
        X, y, test_size=0.25, random_state=mbegu, stratify=y)
    mchoro = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
        ("nb", MultinomialNB()),
    ])
    mchoro.fit(X_mafunzo, y_mafunzo)
    makadirio = mchoro.predict(X_test)
    dok = {
        "usahihi": accuracy_score(y_test, makadirio),
        "ripoti": classification_report(y_test, makadirio,
                                        zero_division=0),
        "matrix": confusion_matrix(y_test, makadirio,
                                   labels=["ham", "spam"]).tolist(),
        "jumla": len(X),
        "mafunzo": len(X_mafunzo),
        "mtihani": len(X_test),
        "maneno": len(mchoro.named_steps["tfidf"].vocabulary_),
        "mchoro": mchoro,
    }
    with open(model_njia, "wb") as f:
        pickle.dump(mchoro, f)
    return dok


def pakua_model(model_njia=None):
    if model_njia is None:
        model_njia = MODEL
    if not os.path.exists(model_njia):
        raise FileNotFoundError(
            "Model haipo - endesha 'fundisha' kwanza")
    with open(model_njia, "rb") as f:
        return pickle.load(f)


def angalia(ujumbe, model_njia=None):
    mchoro = pakua_model(model_njia)
    aina = mchoro.predict([ujumbe])[0]
    ol = dict(zip(mchoro.classes_,
                  mchoro.predict_proba([ujumbe])[0]))
    return {"aina": aina, "uwezo": float(max(ol.values())) * 100}


def thibitisha(njia=None, model_njia=None, mbegu=MBEGU):
    mchoro = pakua_model(model_njia)
    X, y = pakua_data(njia)
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.25, random_state=mbegu, stratify=y)
    makadirio = mchoro.predict(X_test)
    return {"usahihi": accuracy_score(y_test, makadirio),
            "ripoti": classification_report(y_test, makadirio,
                                            zero_division=0)}


def maswali(mambo=None):
    m = argparse.ArgumentParser(
        prog="mielelezo.py",
        description="Mielelezo: spam predictor (sklearn, offline)")
    sub = m.add_subparsers(dest="amri", required=True)
    sub.add_parser("fundisha", help="Fundisha model + hifadhi model.pkl")
    p = sub.add_parser("angalia", help="Tabiri: spam au ham?")
    p.add_argument("ujumbe")
    sub.add_parser("thibitisha", help="Onyesha metriki za mtihani")
    return m


def endesha(mambo):
    if mambo.amri == "fundisha":
        d = fundisha()
        print("IMEFUNDISHWA: mifano %d (mafunzo %d / mtihani %d)"
              % (d["jumla"], d["mafunzo"], d["mtihani"]))
        print("Usahihi wa mtihani: %.1f%%" % (d["usahihi"] * 100))
        print("Maneno: %d" % d["maneno"])
        print(d["ripoti"])
        print("Matrix (nyaya=halisi [[ham,spam],[ham,spam]]):")
        for mstari in d["matrix"]:
            print("  ", mstari)
        print("Model IMEHIFADHIWA: %s" % MODEL)
        return 0

    if mambo.amri == "angalia":
        try:
            m = angalia(mambo.ujumbe)
        except FileNotFoundError as e:
            print("HITILAFU: %s" % e)
            return 1
        print('"%s"' % mambo.ujumbe)
        print("-> %s (uwezo: %.1f%%)" % (m["aina"].upper(), m["uwezo"]))
        return 0

    if mambo.amri == "thibitisha":
        try:
            d = thibitisha()
        except FileNotFoundError as e:
            print("HITILAFU: %s" % e)
            return 1
        print("Usahihi: %.1f%%" % (d["usahihi"] * 100))
        print(d["ripoti"])
        return 0
    return 1


def main(mambo=None):
    p = maswali()
    args = p.parse_args(mambo)
    try:
        return endesha(args)
    except (ValueError, FileNotFoundError) as e:
        print("HITILAFU: %s" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
