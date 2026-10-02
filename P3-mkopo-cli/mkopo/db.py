import csv
import os
import sqlite3
from datetime import datetime

from .models import (
    Mkopo,
    thibitisha_jina,
    thibitisha_kiasi,
    thibitisha_riba,
    thibitisha_miezi,
    thibitisha_aina,
)

MJI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB = os.path.join(MJI, "mkopo.db")
LOG_FILE = os.path.join(MJI, "logs.csv")


def fungua(path=None):
    conn = sqlite3.connect(path or DEFAULT_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def tengeneza(path=None):
    with fungua(path) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS wateja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jina TEXT NOT NULL UNIQUE,
            simu TEXT DEFAULT '',
            tangu TEXT DEFAULT (date('now'))
        );
        CREATE TABLE IF NOT EXISTS mikopo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mteja_id INTEGER NOT NULL,
            kiasi REAL NOT NULL,
            riba REAL NOT NULL,
            miezi INTEGER NOT NULL,
            aina TEXT NOT NULL DEFAULT 'reducing',
            tangu TEXT DEFAULT (date('now')),
            FOREIGN KEY (mteja_id) REFERENCES wateja(id) ON DELETE CASCADE
        );
        """)


def hifadhi_mteja(jina, simu="", path=None):
    jina = thibitisha_jina(jina)
    with fungua(path) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO wateja (jina, simu) VALUES (?, ?)",
            (jina, str(simu).strip()))
        row = conn.execute(
            "SELECT id FROM wateja WHERE jina = ?", (jina,)).fetchone()
        return row["id"]


def hifadhi_mkopo(mteja_id, kiasi, riba, miezi, aina="reducing", path=None):
    m = Mkopo(kiasi, riba, miezi, aina, mteja_id)
    with fungua(path) as conn:
        row = conn.execute(
            "SELECT id FROM wateja WHERE id = ?", (mteja_id,)).fetchone()
        if row is None:
            raise ValueError(
                "Mteja (id=%s) haipo - ongeza kwanza na: main.py ongeza --jina ..."
                % mteja_id)
        cur = conn.execute(
            "INSERT INTO mikopo (mteja_id, kiasi, riba, miezi, aina) "
            "VALUES (?, ?, ?, ?, ?)",
            (mteja_id, m.kiasi, m.riba, m.miezi, m.aina))
        return cur.lastrowid


def orodha_mikopo(path=None):
    with fungua(path) as conn:
        rows = conn.execute("""
            SELECT m.id, w.jina AS mteja, m.kiasi, m.riba, m.miezi,
                   m.aina, m.tangu
            FROM mikopo m
            JOIN wateja w ON w.id = m.mteja_id
            ORDER BY m.id
        """).fetchall()
        return [dict(r) for r in rows]


def orodha_wateja(path=None):
    with fungua(path) as conn:
        rows = conn.execute("""
            SELECT w.id, w.jina, w.simu,
                   COUNT(m.id) AS idadi,
                   COALESCE(SUM(m.kiasi), 0) AS jumla_kiasi
            FROM wateja w
            LEFT JOIN mikopo m ON m.mteja_id = w.id
            GROUP BY w.id
            ORDER BY w.id
        """).fetchall()
        return [dict(r) for r in rows]


def pata_mkopo(kopo_id, path=None):
    with fungua(path) as conn:
        row = conn.execute("""
            SELECT m.id, m.mteja_id, w.jina AS mteja, m.kiasi, m.riba,
                   m.miezi, m.aina, m.tangu
            FROM mikopo m
            JOIN wateja w ON w.id = m.mteja_id
            WHERE m.id = ?
        """, (kopo_id,)).fetchone()
        if row is None:
            raise ValueError("Mkopo (id=%s) haupo" % kopo_id)
        return dict(row)


def futa_mkopo(kopo_id, path=None):
    with fungua(path) as conn:
        cur = conn.execute("DELETE FROM mikopo WHERE id = ?", (kopo_id,))
        return cur.rowcount > 0


def ripoti(path=None):
    with fungua(path) as conn:
        jumla = conn.execute("""
            SELECT COUNT(*) AS idadi, COALESCE(SUM(kiasi), 0) AS kiasi
            FROM mikopo
        """).fetchone()
        kwa_mteja = conn.execute("""
            SELECT w.jina, SUM(m.kiasi) AS kiasi, COUNT(m.id) AS idadi
            FROM mikopo m
            JOIN wateja w ON w.id = m.mteja_id
            GROUP BY m.mteja_id
            ORDER BY kiasi DESC
        """).fetchall()
        return {
            "idadi": jumla["idadi"],
            "jumla_kiasi": jumla["kiasi"],
            "kwa_mteja": [dict(r) for r in kwa_mteja],
        }


def nani_kakopa_zaidi(path=None):
    with fungua(path) as conn:
        rows = conn.execute("""
            SELECT w.jina, COUNT(m.id) AS idadi, SUM(m.kiasi) AS jumla
            FROM mikopo m
            JOIN wateja w ON w.id = m.mteja_id
            GROUP BY m.mteja_id
            ORDER BY jumla DESC
        """).fetchall()
        return [dict(r) for r in rows]


def jumla_kwa_aina(path=None):
    with fungua(path) as conn:
        rows = conn.execute("""
            SELECT aina, COUNT(*) AS idadi, SUM(kiasi) AS jumla,
                   ROUND(AVG(riba), 2) AS wastani_riba
            FROM mikopo
            GROUP BY aina
            ORDER BY aina
        """).fetchall()
        return [dict(r) for r in rows]


def takwimu(path=None):
    with fungua(path) as conn:
        row = conn.execute("""
            SELECT COUNT(*) AS idadi,
                   COALESCE(AVG(kiasi), 0) AS wastani_kiasi,
                   COALESCE(AVG(riba), 0) AS wastani_riba,
                   COALESCE(MAX(kiasi), 0) AS kubwa,
                   COALESCE(MIN(kiasi), 0) AS ndogo,
                   COALESCE(SUM(kiasi), 0) AS jumla
            FROM mikopo
        """).fetchone()
        return dict(row)


def wateja_bila_mikopo(path=None):
    with fungua(path) as conn:
        rows = conn.execute("""
            SELECT w.id, w.jina
            FROM wateja w
            LEFT JOIN mikopo m ON m.mteja_id = w.id
            WHERE m.id IS NULL
            ORDER BY w.id
        """).fetchall()
        return [dict(r) for r in rows]


def tafuta_jina(sehemu, path=None):
    if not str(sehemu).strip():
        raise ValueError("Andika sehemu ya jina ya kutafuta")
    with fungua(path) as conn:
        rows = conn.execute("""
            SELECT m.id, w.jina AS mteja, m.kiasi, m.riba, m.miezi, m.aina
            FROM mikopo m
            JOIN wateja w ON w.id = m.mteja_id
            WHERE w.jina LIKE ?
            ORDER BY m.id
        """, ("%" + str(sehemu).strip() + "%",)).fetchall()
        return [dict(r) for r in rows]


def mikopo_yanayokaribia_kuisha(salio_miezi=3, path=None):
    if int(salio_miezi) < 0:
        raise ValueError("Salio la miezi halikubaliwi kuwa hasi")
    deseni = ("m.miezi - CAST((julianday('now') - julianday(m.tangu))"
              " / 30 AS INTEGER)")
    with fungua(path) as conn:
        rows = conn.execute("""
            SELECT m.id, w.jina AS mteja, m.miezi, m.kiasi,
                   m.tangu,
                   """ + deseni + """ AS yaliyobaki
            FROM mikopo m
            JOIN wateja w ON w.id = m.mteja_id
            WHERE """ + deseni + """ <= ?
            ORDER BY yaliyobaki, m.id
        """, (int(salio_miezi),)).fetchall()
        return [dict(r) for r in rows]


def badilisha_mkopo(kopo_id, path=None, kiasi=None, riba=None, miezi=None,
                    aina=None, jina=None, simu=None):
    sets, params = [], []
    if kiasi is not None:
        sets.append("kiasi = ?")
        params.append(thibitisha_kiasi(kiasi))
    if riba is not None:
        sets.append("riba = ?")
        params.append(thibitisha_riba(riba))
    if miezi is not None:
        sets.append("miezi = ?")
        params.append(thibitisha_miezi(miezi))
    if aina is not None:
        sets.append("aina = ?")
        params.append(thibitisha_aina(aina))
    if not sets and jina is None and simu is None:
        raise ValueError(
            "Hakuna kitu kubadilisha - chagua: "
            "--kiasi, --riba, --miezi, --aina, --jina au --simu")
    with fungua(path) as conn:
        row = conn.execute(
            "SELECT mteja_id FROM mikopo WHERE id = ?", (kopo_id,)).fetchone()
        if row is None:
            raise ValueError("Mkopo (id=%s) haupo" % kopo_id)
        if sets:
            conn.execute(
                "UPDATE mikopo SET " + ", ".join(sets) + " WHERE id = ?",
                params + [kopo_id])
        if jina is not None:
            jina = thibitisha_jina(jina)
            conn.execute("UPDATE wateja SET jina = ? WHERE id = ?",
                         (jina, row["mteja_id"]))
        if simu is not None:
            conn.execute("UPDATE wateja SET simu = ? WHERE id = ?",
                         (str(simu).strip(), row["mteja_id"]))
    return True


def hamisha_mikopo_csv(jina_la_faili, path=None):
    rows = orodha_mikopo(path)
    with open(jina_la_faili, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "mteja", "kiasi", "riba", "miezi", "aina", "tangu"])
        for r in rows:
            w.writerow([r["id"], r["mteja"], r["kiasi"], r["riba"],
                        r["miezi"], r["aina"], r["tangu"]])
    return len(rows)


def kumbuka(amri, maelezo):
    wala = (not os.path.exists(LOG_FILE)
            or os.path.getsize(LOG_FILE) == 0)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if wala:
            w.writerow(["wakati", "amri", "maelezo"])
        w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    amri, maelezo])


def soma_kumbuka(hadhi=30):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return []
    return rows[-hadhi:]
