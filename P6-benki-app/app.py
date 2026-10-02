import functools
import hmac
import os
import secrets
import sqlite3

from flask import (Flask, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from mkopo_hesabu import hesabu

MJI = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "p6-benki-app-siri-badilisha-kwenye-kazi-halisi"
app.config["DB"] = os.environ.get(
    "BENKI_DB", os.path.join(MJI, "benki.db"))

WATEJA_DEMO = [
    ("admin", "benki123", "admin"),
    ("mpokeaji", "pokea123", "mpokeaji"),
    ("mhasibu", "hesabu123", "mhasibu"),
]


def pata_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DB"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def fungua_db(hitilafu):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def tengeneza_db():
    with open(os.path.join(MJI, "schema.sql"), encoding="utf-8") as f:
        maandishi = f.read()
    db = sqlite3.connect(app.config["DB"])
    db.row_factory = sqlite3.Row
    db.executescript(maandishi)
    fk = db.execute("PRAGMA foreign_key_list(kumbukumbu_za_malipo)").fetchone()
    if fk is not None and (fk[6] or "").upper().replace(" ", "") != "SETNULL":
        db.executescript("""
            DROP TRIGGER IF EXISTS malipo_yaingie;
            ALTER TABLE kumbukumbu_za_malipo RENAME TO kumbuku_zamani;
            CREATE TABLE kumbukumbu_za_malipo (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                mkopo_id INTEGER,
                kiasi    REAL NOT NULL,
                wakati   TEXT DEFAULT (DATETIME('now')),
                FOREIGN KEY (mkopo_id) REFERENCES mikopo(id)
                    ON DELETE SET NULL
            );
            INSERT INTO kumbukumbu_za_malipo (id, mkopo_id, kiasi, wakati)
                SELECT id, mkopo_id, kiasi, wakati FROM kumbuku_zamani;
            DROP TABLE kumbuku_zamani;
            CREATE TRIGGER IF NOT EXISTS malipo_yaingie
            AFTER INSERT ON malipo
            BEGIN
                INSERT INTO kumbukumbu_za_malipo (mkopo_id, kiasi)
                VALUES (NEW.mkopo_id, NEW.kiasi);
            END;
        """)
        db.commit()
    for jina, nenosiri, jukumu in WATEJA_DEMO:
        zipo = db.execute(
            "SELECT 1 FROM watumiaji WHERE jina_la_mtumiaji = ?",
            (jina,)).fetchone()
        if not zipo:
            db.execute(
                "INSERT INTO watumiaji (jina_la_mtumiaji, nenosiri_hash, "
                "jukumu) VALUES (?, ?, ?)",
                (jina, generate_password_hash(nenosiri), jukumu))
    db.commit()
    db.close()


@app.context_processor
def toa_csrf():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    return {"csrf": session["csrf"]}


def linazuia_csrf(f):
    @functools.wraps(f)
    def imesindikwa(*mambo, **vitu):
        if request.method == "POST":
            mpokelewa = request.form.get("_csrf", "")
            iliyohifadhiwa = session.get("csrf", "")
            if not mpokelewa or not hmac.compare_digest(mpokelewa,
                                                        iliyohifadhiwa):
                flash("CSRF token imekataliwa - fomu si salama, jaribu tena",
                      "hitilafu")
                return redirect(request.referrer or url_for("nyumbani"))
        return f(*mambo, **vitu)
    return imesindikwa


def linahitaji_kuingia(f):
    @functools.wraps(f)
    def imesindikwa(*mambo, **vitu):
        if "mtumiaji" not in session:
            flash("Tafadhali ingia kwanza", "onyo")
            return redirect(url_for("ingia"))
        return f(*mambo, **vitu)
    return imesindikwa


def linahitaji_jukumu(*majukumu):
    def kupamba(f):
        @functools.wraps(f)
        def imesindikwa(*mambo, **vitu):
            if "mtumiaji" not in session:
                flash("Tafadhali ingia kwanza", "onyo")
                return redirect(url_for("ingia"))
            if session.get("jukumu") not in majukumu:
                flash("HUNA RUHUSA - jukumu lako (%s) haliruhusu kitendo hiki. "
                      "Inahitaji: %s" % (
                          session.get("jukumu", "hakuna"),
                          ", ".join(majukumu)), "hitilafu")
                return redirect(url_for("nyumbani"))
            return f(*mambo, **vitu)
        return imesindikwa
    return kupamba


@app.template_filter("sarafu")
def sarafu(x):
    return format(round(x), ",.0f")


@app.route("/")
def nyumbani():
    if "mtumiaji" not in session:
        return render_template("landing.html")
    db = pata_db()
    mikopo = db.execute("""
        SELECT m.id, w.jina AS mteja, m.kiasi, m.riba, m.miezi, m.aina,
               m.tangu,
               m.kiasi - COALESCE((
                   SELECT SUM(p.kiasi) FROM malipo p WHERE p.mkopo_id = m.id
               ), 0) AS inayobaki
        FROM mikopo m
        JOIN wateja w ON w.id = m.mteja_id
        ORDER BY m.id DESC
    """).fetchall()
    return render_template("orodha.html", mikopo=mikopo)


@app.route("/ingia", methods=["GET", "POST"])
@linazuia_csrf
def ingia():
    if request.method == "POST":
        jina = request.form.get("jina", "").strip()
        nenosiri = request.form.get("nenosiri", "")
        db = pata_db()
        mtu = db.execute(
            "SELECT * FROM watumiaji WHERE jina_la_mtumiaji = ?",
            (jina,)).fetchone()
        if mtu and check_password_hash(mtu["nenosiri_hash"], nenosiri):
            session.clear()
            session["mtumiaji"] = mtu["jina_la_mtumiaji"]
            session["jukumu"] = mtu["jukumu"]
            flash("Karibu tena, %s!" % mtu["jina_la_mtumiaji"], "nafuu")
            return redirect(url_for("nyumbani"))
        flash("Jina au nenosiri si sahihi", "hitilafu")
    return render_template("ingia.html")


@app.route("/toka")
def toka():
    session.clear()
    flash("Umefanikiwa kutoka", "nafuu")
    return redirect(url_for("ingia"))


@app.route("/badilisha", methods=["GET", "POST"])
@linazuia_csrf
@linahitaji_kuingia
def badilisha():
    if request.method == "POST":
        zamani = request.form.get("zamani", "")
        jipya = request.form.get("jipya", "")
        rudia = request.form.get("rudia", "")
        db = pata_db()
        mtu = db.execute(
            "SELECT * FROM watumiaji WHERE jina_la_mtumiaji = ?",
            (session["mtumiaji"],)).fetchone()
        if not check_password_hash(mtu["nenosiri_hash"], zamani):
            flash("Nenosiri la zamani si sahihi", "hitilafu")
        elif len(jipya) < 6:
            flash("Nenosiri jipya lazima liwe na herufi 6 au zaidi", "hitilafu")
        elif jipya != rudia:
            flash("Nenosiri jipya halilingani na kisagwa", "hitilafu")
        elif jipya == zamani:
            flash("Nenosiri jipya ni kama la zamani", "hitilafu")
        else:
            db.execute(
                "UPDATE watumiaji SET nenosiri_hash = ? WHERE id = ?",
                (generate_password_hash(jipya), mtu["id"]))
            db.commit()
            flash("Nenosiri limebadilishwa kwa mafanikio!", "nafuu")
            return redirect(url_for("nyumbani"))
    return render_template("badilisha.html")


@app.route("/ongeza", methods=["GET", "POST"])
@linazuia_csrf
@linahitaji_jukumu("admin")
def ongeza():
    if request.method == "POST":
        jina = request.form.get("jina", "").strip()
        simu = request.form.get("simu", "").strip()
        try:
            kiasi = float(request.form.get("kiasi", ""))
            riba = float(request.form.get("riba", ""))
            miezi = int(request.form.get("miezi", ""))
            aina = request.form.get("aina", "reducing")
            if not jina:
                raise ValueError("Jina la mteja linahitajika")
            hesabu(aina, kiasi, riba, miezi)
        except ValueError as e:
            flash(str(e), "hitilafu")
            return render_template("ongeza.html")
        db = pata_db()
        mteja = db.execute(
            "SELECT id FROM wateja WHERE simu = ? AND simu != ''",
            (simu,)).fetchone()
        if mteja:
            mteja_id = mteja["id"]
        else:
            cur = db.execute(
                "INSERT INTO wateja (jina, simu) VALUES (?, ?)",
                (jina, simu or None))
            mteja_id = cur.lastrowid
        mtumiaji = db.execute(
            "SELECT id FROM watumiaji WHERE jina_la_mtumiaji = ?",
            (session["mtumiaji"],)).fetchone()
        cur = db.execute(
            "INSERT INTO mikopo (mteja_id, aliyeandika_id, kiasi, riba, "
            "miezi, aina) VALUES (?, ?, ?, ?, ?, ?)",
            (mteja_id, mtumiaji["id"], kiasi, riba, miezi, aina))
        db.commit()
        flash("Mkopo mpya umehifadhiwa (id=%s) kwa %s" % (
            cur.lastrowid, jina), "nafuu")
        return redirect(url_for("nyumbani"))
    return render_template("ongeza.html")


@app.route("/wateja")
@linahitaji_kuingia
def orodha_wateja():
    db = pata_db()
    wateja = db.execute("""
        SELECT w.id, w.jina, w.simu, w.tangu,
               COUNT(m.id) AS mikopo,
               COALESCE(SUM(m.kiasi), 0) AS jumla
        FROM wateja w
        LEFT JOIN mikopo m ON m.mteja_id = w.id
        GROUP BY w.id
        ORDER BY w.jina
    """).fetchall()
    return render_template("wateja.html", wateja=wateja,
                           anaweza_futa=session.get("jukumu") == "admin")


@app.route("/mkopo/<int:kopo_id>")
@linahitaji_kuingia
def jedwali(kopo_id):
    db = pata_db()
    r = db.execute("""
        SELECT m.*, w.jina AS mteja,
               COALESCE((SELECT SUM(p.kiasi) FROM malipo p
                         WHERE p.mkopo_id = m.id), 0) AS imeolishwa
        FROM mikopo m
        JOIN wateja w ON w.id = m.mteja_id
        WHERE m.id = ?
    """, (kopo_id,)).fetchone()
    if r is None:
        flash("Mkopo huo haupo", "hitilafu")
        return redirect(url_for("nyumbani"))
    m = hesabu(r["aina"], r["kiasi"], r["riba"], r["miezi"])
    return render_template("jedwali.html", r=r, m=m,
                           inayobaki=r["kiasi"] - r["imeolishwa"])


@app.route("/mkopo/<int:kopo_id>/lipa", methods=["POST"])
@linazuia_csrf
@linahitaji_jukumu("admin", "mpokeaji")
def lipa(kopo_id):
    try:
        kiasi = float(request.form.get("kiasi", ""))
        if kiasi <= 0:
            raise ValueError("Kiasi lazima liwe zaidi ya 0")
    except ValueError as e:
        flash(str(e) if str(e) else "Kiasi si sahihi", "hitilafu")
        return redirect(url_for("jedwali", kopo_id=kopo_id))
    db = pata_db()
    r = db.execute("""
        SELECT m.kiasi - COALESCE((
            SELECT SUM(p.kiasi) FROM malipo p WHERE p.mkopo_id = m.id
        ), 0) AS inayobaki
        FROM mikopo m WHERE m.id = ?
    """, (kopo_id,)).fetchone()
    if r is None:
        flash("Mkopo haupo", "hitilafu")
        return redirect(url_for("jedwali", kopo_id=kopo_id))
    if kiasi > r["inayobaki"]:
        flash("Kiasi kikubwa kuliko deni lililobaki (%s)" % (
            format(round(r["inayobaki"]), ",.0f")), "hitilafu")
        return redirect(url_for("jedwali", kopo_id=kopo_id))
    njia = request.form.get("njia", "fedha")
    if njia not in ("fedha", "benki", "m-pesa"):
        njia = "fedha"
    db.execute(
        "INSERT INTO malipo (mkopo_id, kiasi, njia) VALUES (?, ?, ?)",
        (kopo_id, kiasi, njia))
    db.commit()
    flash("Malipo %s yamepokelewa - kumbukumbu imeandikwa na database yenyewe "
          "(TRIGGER)!" % format(round(kiasi), ",.0f"), "nafuu")
    return redirect(url_for("jedwali", kopo_id=kopo_id))


@app.route("/mkopo/<int:kopo_id>/futa", methods=["POST"])
@linazuia_csrf
@linahitaji_jukumu("admin")
def futa_mkopo(kopo_id):
    db = pata_db()
    cur = db.execute("DELETE FROM mikopo WHERE id = ?", (kopo_id,))
    db.commit()
    if cur.rowcount:
        flash("Mkopo id=%s umefutwa (na malipo yake yamelandia CASCADE pia!)"
              % kopo_id, "nafuu")
    else:
        flash("Mkopo huo haupo", "hitilafu")
    return redirect(url_for("nyumbani"))


@app.route("/wateja/<int:mteja_id>/futa", methods=["POST"])
@linazuia_csrf
@linahitaji_jukumu("admin")
def futa_mteja(mteja_id):
    db = pata_db()
    try:
        cur = db.execute("DELETE FROM wateja WHERE id = ?", (mteja_id,))
        db.commit()
    except sqlite3.IntegrityError:
        flash("IMEKATAA (RESTRICT): mteja huyu ana mikopo - futa mikopo yake "
              "kwanza", "hitilafu")
        return redirect(url_for("orodha_wateja"))
    if cur.rowcount:
        flash("Mteja id=%s amefutwa" % mteja_id, "nafuu")
    else:
        flash("Mteja huyo haupo", "hitilafu")
    return redirect(url_for("orodha_wateja"))


@app.route("/ripoti")
@linahitaji_jukumu("admin", "mhasibu")
def ripoti():
    db = pata_db()
    jumla = db.execute("""
        SELECT COUNT(*) AS idadi,
               COALESCE(SUM(kiasi), 0) AS kiasi,
               COALESCE(SUM(m.kiasi - COALESCE((
                   SELECT SUM(p.kiasi) FROM malipo p
                   WHERE p.mkopo_id = m.id), 0)), 0) AS deni
        FROM mikopo m
    """).fetchone()
    kwa_mteja = db.execute("""
        SELECT w.jina, SUM(m.kiasi) AS jumla, COUNT(m.id) AS idadi
        FROM mikopo m
        JOIN wateja w ON w.id = m.mteja_id
        GROUP BY m.mteja_id
        ORDER BY jumla DESC
    """).fetchall()
    kumbukumbu = db.execute(
        "SELECT COUNT(*) AS idadi FROM kumbukumbu_za_malipo").fetchone()
    return render_template("ripoti.html", jumla=jumla, kwa_mteja=kwa_mteja,
                           kumbukumbu=kumbukumbu["idadi"])


if __name__ == "__main__":
    tengeneza_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
