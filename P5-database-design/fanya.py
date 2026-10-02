import os
import re
import shutil
import sqlite3
import sys
from datetime import datetime

MJI = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(MJI, "mfumo.db")

PACRA = "-" * 74


def bakuli():
    if not os.path.exists(DB):
        print("Hakuna DB ya nakala bado - endesha: python fanya.py kwanza")
        return
    muda = datetime.now().strftime("%Y%m%d-%H%M%S")
    nakala = os.path.join(MJI, "nakala-%s.db" % muda)
    shutil.copy2(DB, nakala)
    print("NAKALA IMEHIFADHIWA: %s (%d bytes)" % (
        nakala, os.path.getsize(nakala)))


def soma_faili(jina):
    with open(os.path.join(MJI, jina), encoding="utf-8") as f:
        return f.read()


def onyesha(kichwa, safu, matokeo):
    print("\n" + PACRA)
    print(kichwa)
    print(PACRA)
    if not matokeo:
        print("(hakuna matokeo - 0 safu zilizorudi)")
        return
    mpana = [max(len(safu[i]), max(len(str(r[i])) for r in matokeo))
             for i in range(len(safu))]
    print(" | ".join(s.ljust(mpana[i]) for i, s in enumerate(safu)))
    print("-+-".join("-" * m for m in mpana))
    for r in matokeo:
        print(" | ".join(str(r[i]).ljust(mpana[i]) for i in range(len(safu))))


def main():
    if "--backup" in sys.argv:
        bakuli()
        return
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    print("Inatengeneza database: " + DB)
    cur.executescript(soma_faili("schema.sql"))
    cur.executescript(soma_faili("data.sql"))
    conn.commit()
    print("Schema + data: IMEFANIKIWA (4 tables, 1 view, 2 index)")

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' "
                "AND name NOT LIKE 'sqlite_%'")
    vitabu = [r[0] for r in cur.fetchall()]
    for t in vitabu:
        cur.execute("SELECT COUNT(*) FROM " + t)
        n = cur.fetchone()[0]
        print("  - %-10s safu: %d, data: %d" % (t, len(cur.execute(
            "PRAGMA table_info(" + t + ")").fetchall()), n))

    maandishi = soma_faili("queries.sql")
    maandishi = re.sub(r"--[^\n]*", "", maandishi)
    maswali = [s.strip() for s in maandishi.split(";") if s.strip()]
    namba = 0
    for swali in maswali:
        namba += 1
        cur.execute(swali)
        safu = [d[0] for d in cur.description]
        matokeo = cur.fetchall()
        kichwa = swali.split("\n")[0].strip()
        if len(kichwa) > 70:
            kichwa = kichwa[:70] + "..."
        onyesha("SWALI %d: %s" % (namba, kichwa), safu, matokeo)

    print("\n" + PACRA)
    print("JARIBIO LA ULINZI (CHECK/UNIQUE/FOREIGN KEY) - database lazima ikatae!")
    print(PACRA)
    majaribio = [
        ("kiasi hasi (-5000)",
         "INSERT INTO mikopo (mteja_id, aliyeandika_id, kiasi, riba, miezi, aina)"
         " VALUES (1, 1, -5000, 10, 12, 'flat')"),
        ("aina isiyojulikana ('halali')",
         "INSERT INTO mikopo (mteja_id, aliyeandika_id, kiasi, riba, miezi, aina)"
         " VALUES (1, 1, 100000, 10, 12, 'halali')"),
        ("simu iliyoshahiwa (UNIQUE)",
         "INSERT INTO wateja (jina, simu) VALUES ('Mtu Mpya', '0712345678')"),
        ("mteja asiyekuwepo (FK id=99)",
         "INSERT INTO mikopo (mteja_id, aliyeandika_id, kiasi, riba, miezi, aina)"
         " VALUES (99, 1, 100000, 10, 12, 'flat')"),
        ("jukumu isiyo halali (CHECK)",
         "INSERT INTO watumiaji (jina_la_mtumiaji, nenosiri_hash, jukumu)"
         " VALUES ('mtu', 'h', 'mfalme')"),
    ]
    idadi_imekataa = 0
    for jina, sql in majaribio:
        try:
            cur.execute(sql)
            print("  [HATARI] %s -> IMEKUBALIWA (haipaswi!)" % jina)
        except sqlite3.IntegrityError as e:
            idadi_imekataa += 1
            print("  [SAWA] %s -> IMEKATAA: %s" % (jina, e))
    print("  Jumla imekataa: %d kati ya %d" % (
        idadi_imekataa, len(majaribio)))

    cur.execute("SELECT COUNT(*) FROM kumbukumbu_za_malipo")
    nk = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM malipo")
    nm = cur.fetchone()[0]
    print("\n" + PACRA)
    print("TRIGGER (kumbukumbu OTOMATIKI)")
    print(PACRA)
    print("Malipo yaliyoingia: %d | Kumbukumbu zilizoandikwa na DB yenyewe: %d"
          % (nm, nk))
    print("(hakuna code ya Python iliyohitajika - TRIGGER ndiyo iliyofanya!)")
    cur.execute("SELECT mkopo_id, kiasi, wakati FROM kumbukumbu_za_malipo "
                "ORDER BY id DESC LIMIT 3")
    for r in cur.fetchall():
        print("  mkopo=%s kiasi=%s wakati=%s" % r)

    conn.commit()
    conn.close()
    print("\n" + PACRA)
    print("IMEKAMILIKA. DB: mfumo.db | Nakala: python fanya.py --backup")
    print(PACRA)


if __name__ == "__main__":
    main()
