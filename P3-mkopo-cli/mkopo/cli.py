import argparse
import csv
import os
import sys

from . import db
from .amortization import hesabu


def sarafu(x):
    return format(round(x), ",.0f")


def rangi(text, code):
    return "\033[%sm%s\033[0m" % (code, text)


def onyesha_jedwali(matokeo):
    print("--- JEDWALI LA MALIPO (%s) ---" % matokeo["aina"].upper())
    print("Mwezi |     Malipo |       Riba |  Marejesho |      Salio")
    print("------+------+------------+------------+------------")
    for r in matokeo["jedwali"]:
        print("%5d | %10s | %10s | %10s | %10s" % (
            r["mwezi"], sarafu(r["malipo"]), sarafu(r["riba"]),
            sarafu(r["marejesho"]), sarafu(r["salio"])))
    print("Riba ya jumla: %s | Jumla ya deni: %s | Malipo/mwezi: %s" % (
        sarafu(matokeo["riba_ya_jumla"]), sarafu(matokeo["jumla"]),
        sarafu(matokeo["malipo_mwezi"])))


def amri_ongeza(a, path):
    mteja_id = db.hifadhi_mteja(a.jina, a.simu, path)
    kopo_id = db.hifadhi_mkopo(
        mteja_id, a.kiasi, a.riba, a.miezi, a.aina, path)
    m = hesabu(a.aina, a.kiasi, a.riba, a.miezi)
    print(rangi("Imehifadhiwa: mkopo id=%s kwa %s" % (kopo_id, a.jina), "32"))
    print("Riba ya jumla: %s | Jumla: %s | Malipo/mwezi: %s" % (
        sarafu(m["riba_ya_jumla"]), sarafu(m["jumla"]),
        sarafu(m["malipo_mwezi"])))
    print("Jedwali: main.py jadwali %s" % kopo_id)
    db.kumbuka("ongeza", "mkopo id=%s kwa %s kiasi=%s riba=%s%% miezi=%s %s" % (
        kopo_id, a.jina, sarafu(a.kiasi), a.riba, a.miezi, a.aina))


def amri_wateja(a, path):
    rows = db.orodha_wateja(path)
    if not rows:
        print("Hakuna wateja bado - ongeza na: main.py ongeza --jina ...")
        return
    print("ID | JMNA             | SIMU      | MIKOPO | JUMLA KIASI")
    print("---+------------------+-----------+--------+-------------")
    for r in rows:
        print("%2d | %-16s | %-9s | %6d | %12s" % (
            r["id"], r["jina"][:16], r["simu"] or "-", r["idadi"],
            sarafu(r["jumla_kiasi"])))


def amri_orodha(a, path):
    rows = db.orodha_mikopo(path)
    if not rows:
        print("Hakuna mikopo bado - ongeza na: main.py ongeza ...")
        return
    print("ID | MTEJA            | KIASI | RIBA | MIEZI | AINA")
    print("---+------------------+-------+------+------+------------")
    for r in rows:
        print("%2d | %-16s | %5s | %4s | %5d | %s" % (
            r["id"], r["mteja"][:16], sarafu(r["kiasi"]),
            "%s%%" % r["riba"], r["miezi"], r["aina"]))


def amri_jadwali(a, path):
    r = db.pata_mkopo(a.id, path)
    print("Mkopo id=%s | Mteja: %s | %s @ %s%% x %s miezi (%s)" % (
        r["id"], r["mteja"], sarafu(r["kiasi"]), r["riba"],
        r["miezi"], r["aina"]))
    onyesha_jedwali(hesabu(r["aina"], r["kiasi"], r["riba"], r["miezi"]))


def amri_ripoti(a, path):
    r = db.ripoti(path)
    print("MIKOPO: %d | JUMLA YA KIASI: %s TZS" % (
        r["idadi"], sarafu(r["jumla_kiasi"])))
    if r["kwa_mteja"]:
        print("MTEJA ANAYEDEAI ZAIDI: %s (%s TZS)" % (
            r["kwa_mteja"][0]["jina"], sarafu(r["kwa_mteja"][0]["kiasi"])))
    for x in r["kwa_mteja"]:
        print("  %-16s mikopo=%d jumla=%s" % (
            x["jina"], x["idadi"], sarafu(x["kiasi"])))


def amri_futa(a, path):
    if db.futa_mkopo(a.id, path):
        print(rangi("Mkopo id=%s umefutwa" % a.id, "33"))
        db.kumbuka("futa", "mkopo id=%s umefutwa" % a.id)
    else:
        print("Mkopo id=%s haupo" % a.id)


def amri_badilisha(a, path):
    idadi = sum(1 for x in (a.kiasi, a.riba, a.miezi, a.aina, a.jina, a.simu)
                if x is not None)
    if idadi == 0:
        raise ValueError(
            "Chagua kitu kubadilisha: --kiasi, --riba, --miezi, "
            "--aina, --jina au --simu")
    db.badilisha_mkopo(a.id, path, kiasi=a.kiasi, riba=a.riba,
                       miezi=a.miezi, aina=a.aina, jina=a.jina, simu=a.simu)
    r = db.pata_mkopo(a.id, path)
    print(rangi("Imebadilishwa: mkopo id=%s" % a.id, "32"))
    print("%s | %s @ %s%% x %s miezi (%s)" % (
        r["mteja"], sarafu(r["kiasi"]), r["riba"], r["miezi"], r["aina"]))
    m = hesabu(r["aina"], r["kiasi"], r["riba"], r["miezi"])
    print("Jumla sasa: %s | Malipo/mwezi: %s" % (
        sarafu(m["jumla"]), sarafu(m["malipo_mwezi"])))
    db.kumbuka("badilisha", "mkopo id=%s -> kiasi=%s riba=%s%% miezi=%s %s" % (
        a.id, sarafu(r["kiasi"]), r["riba"], r["miezi"], r["aina"]))


def amri_hamisha(a, path):
    if a.jadwali is not None:
        r = db.pata_mkopo(a.jadwali, path)
        faili = a.faili or os.path.join(db.MJI, "jadwali-%s.csv" % r["id"])
        m = hesabu(r["aina"], r["kiasi"], r["riba"], r["miezi"])
        with open(faili, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["mwezi", "malipo", "riba", "marejesho", "salio"])
            for j in m["jedwali"]:
                w.writerow([j["mwezi"], round(j["malipo"], 2),
                            round(j["riba"], 2), round(j["marejesho"], 2),
                            round(j["salio"], 2)])
        n = len(m["jedwali"])
        maneno = "jedwali la mkopo id=%s" % r["id"]
    else:
        faili = a.faili or os.path.join(db.MJI, "mikopo.csv")
        n = db.hamisha_mikopo_csv(faili, path)
        maneno = "mikopo yote (%d)" % n
    print(rangi("Imehifadhiwa: %s (mistari %d)" % (faili, n), "32"))
    db.kumbuka("hamisha", "%s -> %s" % (maneno, faili))


def amri_kumbuka(a, path):
    rows = db.soma_kumbuka(hadhi=a.idipvo)
    if not rows:
        print("Hakuna kumbukumbu bado")
        return
    for r in rows:
        print(" | ".join(r))


def amri_hoji(a, path):
    while True:
        print("\n=== HOJI: Maswali ya DATA (SQL queries) ===")
        print("1. Nani kakopa zaidi? (ranking)")
        print("2. Jumla kwa aina (flat vs reducing)")
        print("3. Takwimu: wastani, kubwa, ndogo, jumla")
        print("4. Wateja wasio na mikopo (bado)")
        print("5. Tafuta kwa jina (sehemu)")
        print("6. Mikopo inayokaribia kuisha (miezi 3)")
        print("0. Rudi kwenye amri")
        ch = input("Swali: ").strip()
        try:
            if ch == "1":
                rows = db.nani_kakopa_zaidi(path)
                if not rows:
                    print("Hakuna mikopo bado")
                    continue
                print("Nani kakopa zaidi:")
                for n, r in enumerate(rows, 1):
                    print("%2d. %-18s mikopo=%d  jumla=%s" % (
                        n, r["jina"], r["idadi"], sarafu(r["jumla"])))
            elif ch == "2":
                rows = db.jumla_kwa_aina(path)
                if not rows:
                    print("Hakuna mikopo bado")
                    continue
                print("Aina | idadi | jumla kiasi | wastani riba")
                print("-----+-------+-------------+-------------")
                for r in rows:
                    print("%-6s | %5d | %11s | %s%%" % (
                        r["aina"], r["idadi"], sarafu(r["jumla"]),
                        r["wastani_riba"]))
            elif ch == "3":
                t = db.takwimu(path)
                if t["idadi"] == 0:
                    print("Hakuna mikopo bado")
                    continue
                print("MIKOPO: %d" % t["idadi"])
                print("JUMLA: %s | WASTANI: %s | KUBWA: %s | NDOGO: %s" % (
                    sarafu(t["jumla"]), sarafu(t["wastani_kiasi"]),
                    sarafu(t["kubwa"]), sarafu(t["ndogo"])))
                print("WASTANI WA RIBA: %.2f%%" % t["wastani_riba"])
            elif ch == "4":
                rows = db.wateja_bila_mikopo(path)
                if not rows:
                    print("Kila mteja ana mkopo wake")
                    continue
                print("Wateja wasio na mikopo:")
                for r in rows:
                    print("  %2d. %s" % (r["id"], r["jina"]))
            elif ch == "5":
                sehemu = input("Sehemu ya jina (mf. 'ash'): ").strip()
                rows = db.tafuta_jina(sehemu, path)
                if not rows:
                    print("Hakuna anayelingana na: %s" % sehemu)
                    continue
                print("Matokeo (%d):" % len(rows))
                for r in rows:
                    print("  id=%-2d %-18s %s @ %s%% x %s (%s)" % (
                        r["id"], r["mteja"], sarafu(r["kiasi"]),
                        r["riba"], r["miezi"], r["aina"]))
            elif ch == "6":
                rows = db.mikopo_yanayokaribia_kuisha(3, path)
                if not rows:
                    print("Hakuna mkopo unaoisha ndani ya miezi 3")
                    continue
                print("Mikopo inayoisha (salio la miezi):")
                for r in rows:
                    print("  id=%-2d %-18s yaliyobaki=%d miezi (jumla %s)" % (
                        r["id"], r["mteja"], r["yaliyobaki"],
                        sarafu(r["kiasi"])))
            elif ch == "0":
                return
            else:
                print("Chaguo si sahihi - jaribu tena")
        except ValueError as e:
            print(rangi("Hitilafu: %s" % e, "31"))
        except (EOFError, KeyboardInterrupt):
            print("")
            return


def menyu(path):
    db.tengeneza(path)
    while True:
        print("\n=== MKOPO CLI PRO ===")
        print("1. Ongeza mteja na mkopo")
        print("2. Wateja")
        print("3. Mikopo yote")
        print("4. Jedwali la malipo")
        print("5. Ripoti")
        print("6. Futa mkopo")
        print("7. Maswali ya data (hoji)")
        print("8. Badilisha mkopo")
        print("9. Hamisha CSV")
        print("10. Kumbukumbu (logs)")
        print("0. Toka")
        ch = input("Chaguo: ").strip()
        try:
            if ch == "1":
                jina = input("Jina la mteja: ")
                simu = input("Simu (hiari): ")
                kiasi = float(input("Kiasi cha mkopo (TZS): "))
                riba = float(input("Riba kwa mwaka (%): "))
                miezi = int(input("Muda wa malipo (miezi): "))
                aina = input("Aina [flat/reducing] (bofya ENTER = reducing): ").strip() or "reducing"
                a = argparse.Namespace(
                    jina=jina, simu=simu, kiasi=kiasi, riba=riba,
                    miezi=miezi, aina=aina)
                amri_ongeza(a, path)
            elif ch == "2":
                amri_wateja(None, path)
            elif ch == "3":
                amri_orodha(None, path)
            elif ch == "4":
                i = int(input("ID ya mkopo: "))
                amri_jadwali(argparse.Namespace(id=i), path)
            elif ch == "5":
                amri_ripoti(None, path)
            elif ch == "6":
                i = int(input("ID ya mkopo kufuta: "))
                amri_futa(argparse.Namespace(id=i), path)
            elif ch == "7":
                amri_hoji(None, path)
            elif ch == "8":
                i = int(input("ID ya mkopo: "))
                print("1=kiasi 2=riba 3=miezi 4=aina 5=jina 6=simu")
                ch2 = input("Kitu gani: ").strip()
                majina = {"1": "kiasi", "2": "riba", "3": "miezi",
                          "4": "aina", "5": "jina", "6": "simu"}
                if ch2 not in majina:
                    print("Chaguo si sahihi")
                    continue
                jibu = input("Thamani mpya: ")
                if majina[ch2] in ("kiasi", "riba"):
                    jibu = float(jibu)
                elif majina[ch2] == "miezi":
                    jibu = int(jibu)
                vidu = {"id": i, "kiasi": None, "riba": None, "miezi": None,
                        "aina": None, "jina": None, "simu": None}
                vidu[majina[ch2]] = jibu
                amri_badilisha(argparse.Namespace(**vidu), path)
            elif ch == "9":
                amri_hamisha(argparse.Namespace(faili=None, jadwali=None),
                             path)
            elif ch == "10":
                amri_kumbuka(argparse.Namespace(idipvo=30), path)
            elif ch == "0":
                print("Kwaheri!")
                return
            else:
                print("Chaguo si sahihi - jaribu tena")
        except ValueError as e:
            print(rangi("Hitilafu: %s - jaribu tena" % e, "31"))
        except (EOFError, KeyboardInterrupt):
            print("\nKwaheri!")
            return


def kuu():
    os.system("")
    p = argparse.ArgumentParser(
        prog="mkopo", description="Mfumo wa Mikopo CLI Pro (P3)")
    p.add_argument("--db", default=None,
                   help="njia ya faili la SQLite (default: mkopo.db)")
    sub = p.add_subparsers(dest="amri")

    s = sub.add_parser("ongeza", help="ongeza mteja/mkopo")
    s.add_argument("--jina", required=True)
    s.add_argument("--simu", default="")
    s.add_argument("--kiasi", type=float, required=True)
    s.add_argument("--riba", type=float, required=True)
    s.add_argument("--miezi", type=int, required=True)
    s.add_argument("--aina", choices=["flat", "reducing"], default="reducing")
    s.set_defaults(f=amri_ongeza)

    s = sub.add_parser("wateja", help="orodha ya wateja")
    s.set_defaults(f=amri_wateja)

    s = sub.add_parser("orodha", help="orodha ya mikopo yote")
    s.set_defaults(f=amri_orodha)

    s = sub.add_parser("jadwali", help="jedwali la malipo")
    s.add_argument("id", type=int)
    s.set_defaults(f=amri_jadwali)

    s = sub.add_parser("ripoti", help="muhtasari wa mikopo")
    s.set_defaults(f=amri_ripoti)

    s = sub.add_parser("futa", help="futa mkopo")
    s.add_argument("id", type=int)
    s.set_defaults(f=amri_futa)

    s = sub.add_parser("hoji", help="maswali ya data (SQL queries)")
    s.set_defaults(f=amri_hoji)

    s = sub.add_parser("badilisha", help="hariri mkopo/mteja (UPDATE)")
    s.add_argument("id", type=int)
    s.add_argument("--kiasi", type=float)
    s.add_argument("--riba", type=float)
    s.add_argument("--miezi", type=int)
    s.add_argument("--aina", choices=["flat", "reducing"])
    s.add_argument("--jina", help="jina jipya la mteja")
    s.add_argument("--simu", help="simu mpya ya mteja")
    s.set_defaults(f=amri_badilisha)

    s = sub.add_parser("hamisha", help="hamisha CSV (Excel)")
    s.add_argument("--faili", default=None, help="jina la faili la CSV")
    s.add_argument("--jadwali", type=int, default=None,
                   help="hamisha jedwali la mkopo huu badala ya orodha")
    s.set_defaults(f=amri_hamisha)

    s = sub.add_parser("kumbuka", help="onyesha kumbukumbu za amri (logs)")
    s.add_argument("--idipvo", type=int, default=30,
                   help="idadi ya mistari (default 30)")
    s.set_defaults(f=amri_kumbuka)

    s = sub.add_parser("menyu", help="menyu ya kubonyeza (GUI rahisi)")
    s.set_defaults(f=lambda a, path: menyu(path))

    a = p.parse_args()
    if not hasattr(a, "f"):
        p.print_help()
        print("\nMfano:")
        print("  python main.py menyu")
        print("  python main.py ongeza --jina \"Juma\" --kiasi 100000 "
              "--riba 15 --miezi 6")
        print("  python main.py jadwali 1")
        return
    try:
        db.tengeneza(a.db)
        a.f(a, a.db)
    except ValueError as e:
        print(rangi("Hitilafu: %s" % e, "31"))
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nIliagwa")
        sys.exit(130)
