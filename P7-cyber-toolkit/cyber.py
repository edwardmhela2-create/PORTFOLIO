import argparse
import base64
import hashlib
import hmac
import ipaddress
import math
import os
import random
import secrets
import socket
import string
import sys
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

PORTA_ZINAZOJULIKANA = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
    80: "http", 110: "pop3", 135: "rpc", 139: "netbios", 143: "imap",
    443: "https", 445: "smb", 993: "imaps", 995: "pop3s",
    3306: "mysql", 3389: "rdp", 5432: "postgres", 6379: "redis",
    8080: "http-alt", 8443: "https-alt",
}
NEMBO_DHAIFU = {
    "123456", "password", "qwerty", "admin", "12345678", "123456789",
    "iloveyou", "monkey", "letmein", "welcome", "benki123", "abc123",
}


def hesabu_hash(mzigo, aina="sha256"):
    h = hashlib.new(aina)
    h.update(mzigo)
    return h.hexdigest()


def hash_file(njia, aina="sha256", kipimo=65536):
    h = hashlib.new(aina)
    with open(njia, "rb") as f:
        kwa = f.read(kipimo)
        while kwa:
            h.update(kwa)
            kwa = f.read(kipimo)
    return h.hexdigest()


def siri_mandishi(lengo, fumbo):
    if not fumbo:
        raise ValueError("Funguo inahitajika")
    lb = lengo.encode("utf-8")
    fb = fumbo.encode("utf-8")
    ghafi = bytes(lb[i] ^ fb[i % len(fb)] for i in range(len(lb)))
    muhuri = hmac.new(fb, ghafi, hashlib.sha256).digest()
    return base64.b64encode(muhuri + ghafi).decode("ascii")


def fungua_mandishi(doa, fumbo):
    if not fumbo:
        raise ValueError("Funguo inahitajika")
    try:
        kilichoingia = base64.b64decode(doa, validate=True)
    except Exception:
        raise ValueError("Si base64 sahihi")
    if len(kilichoingia) < 32:
        raise ValueError("Maandishi mafupi mno")
    muhuri, ghafi = kilichoingia[:32], kilichoingia[32:]
    fb = fumbo.encode("utf-8")
    inayotarajiwa = hmac.new(fb, ghafi, hashlib.sha256).digest()
    if not hmac.compare_digest(muhuri, inayotarajiwa):
        raise ValueError("Funguo si sahihi AU maandishi yameharibika")
    toa = bytes(ghafi[i] ^ fb[i % len(fb)] for i in range(len(ghafi)))
    try:
        return toa.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Maandishi yameharibika")


def tengeneza_nenosiri(urefu=16):
    if urefu < 4:
        raise ValueError("Urefu lazima uwe 4 au zaidi")
    herufi_kubwa = string.ascii_uppercase
    herufi_ndogo = string.ascii_lowercase
    namba = string.digits
    alama = "!@#$%^&*()-_=+[]{}"
    zote = herufi_kubwa + herufi_ndogo + namba + alama
    mratibu = random.SystemRandom()
    neno = [mratibu.choice(p) for p in (herufi_kubwa, herufi_ndogo,
                                        namba, alama)]
    neno += [mratibu.choice(zote) for _ in range(urefu - 4)]
    mratibu.shuffle(neno)
    return "".join(neno)


def imarisha_nenosiri(neno):
    mapendekezo = []
    alama = 0
    if neno.lower() in NEMBO_DHAIFU:
        return {"alama": 0, "hukumu": "MBOVU - nembo inajulikana kwa wizi!",
                "entropy": 0.0, "mapendekezo": ["Badilisha kabisa"]}
    if len(neno) >= 8:
        alama += 1
    else:
        mapendekezo.append("Urefu: angalau herufi 8 (bora 12+)")
    if len(neno) >= 12:
        alama += 1
    if any(c.isupper() for c in neno):
        alama += 1
    else:
        mapendekezo.append("Ongeza herufi kubwa (A-Z)")
    if any(c.islower() for c in neno):
        alama += 1
    else:
        mapendekezo.append("Ongeza herufi ndogo (a-z)")
    if any(c.isdigit() for c in neno):
        alama += 1
    else:
        mapendekezo.append("Ongeza namba (0-9)")
    if any(not c.isalnum() for c in neno):
        alama += 1
    else:
        mapendekezo.append("Ongeza alama maalum (!@#...)")
    kipengele = 0
    if any(c.isupper() for c in neno):
        kipengele += 26
    if any(c.islower() for c in neno):
        kipengele += 26
    if any(c.isdigit() for c in neno):
        kipengele += 10
    if any(not c.isalnum() for c in neno):
        kipengele += 26
    entropy = math.log2(kipengele) * len(neno) if kipengele else 0.0
    if alama <= 1:
        hukumu = "MBOVU"
    elif alama <= 3:
        hukumu = "DHAIFU"
    elif alama <= 5:
        hukumu = "WASTANI"
    else:
        hukumu = "IMARA"
    if not mapendekezo:
        mapendekezo.append("Vizuri! Endelea hivyo")
    return {"alama": alama, "hukumu": hukumu, "entropy": entropy,
            "mapendekezo": mapendekezo}


def ip_funguo(mwako):
    try:
        ip = ipaddress.ip_address(mwako)
    except ValueError:
        raise ValueError("Si IP sahihi: %s" % mwako)
    return {
        "ip": str(ip), "version": ip.version,
        "private": ip.is_private, "loopback": ip.is_loopback,
        "link_local": ip.is_link_local, "multicast": ip.is_multicast,
        "global": ip.is_global, "reserved": ip.is_reserved,
    }


def jaribu_port(host, port, muda):
    try:
        k = socket.create_connection((host, port), timeout=muda)
        k.close()
        return port
    except OSError:
        return None


def chunguza_ports(host, porta, muda=0.5):
    wazi = []
    with ThreadPoolExecutor(max_workers=100) as kazi:
        kwa = {kazi.submit(jaribu_port, host, p, muda): p for p in porta}
        for f in as_completed(kwa):
            r = f.result()
            if r:
                wazi.append(r)
    return sorted(wazi)


def anzia_soketi(urefu=0.5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    s.settimeout(urefu)
    return s


def jenga_porta(a=None, mzigo=None):
    if a:
        return [int(x) for x in a.split(",") if x.strip()]
    if mzigo:
        if "-" not in mzigo:
            raise ValueError("Mzigo sahihi: 1-1024")
        mwanzo, mwisho = mzigo.split("-")
        porta = list(range(int(mwanzo), int(mwisho) + 1))
        if len(porta) > 5000:
            raise ValueError("Mzigo mkubwa mno (max 5000)")
        return porta
    return list(PORTA_ZINAZOJULIKANA)


def andika_ripoti(host, wazi, zote, njia="ripoti-cyber.html"):
    sasa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mistari = []
    for p in wazi:
        jina = PORTA_ZINAZOJULIKANA.get(p, "?")
        mistari.append(
            "<tr><td>%d</td><td>%s</td><td class='wazi'>WAZI</td></tr>"
            % (p, jina))
    if not mistari:
        mistari.append("<tr><td colspan='3'>Hakuna port "
                       "iliyofunguliwa</td></tr>")
    html = (
        "<!DOCTYPE html>\n<html lang='sw'><head><meta charset='utf-8'>"
        "<title>Ripoti ya Ports - %s</title><style>"
        "body{font-family:'Segoe UI',sans-serif;background:#f6f8fb;"
        "color:#1b2a4a;max-width:800px;margin:30px auto;padding:0 16px}"
        "h1{background:#1b2a4a;color:#fff;padding:16px 20px;"
        "border-radius:10px;font-size:22px}"
        "table{width:100%%;border-collapse:collapse;background:#fff}"
        "th{background:#1b2a4a;color:#fff;padding:9px;text-align:left}"
        "td{padding:9px;border-bottom:1px solid #d9e1ec}"
        ".wazi{color:#1f9d55;font-weight:700}"
        ".lebo{color:#667;font-size:14px}"
        ".ethics{background:#fff7e0;border:1px solid #f0b429;padding:10px;"
        "border-radius:8px;margin-top:16px;font-size:14px}"
        "</style></head><body>"
        "<h1>Ripoti ya Ports - %s</h1>"
        "<p class='lebo'>Host: <b>%s</b> | Tarehe: %s | "
        "Ilichunguzwa: %d | <b class='wazi'>WAZI: %d</b> | "
        "Zilizofungwa: %d</p>"
        "<table><tr><th>Port</th><th>Huduma</th><th>Hali</th></tr>%s"
        "</table>"
        "<div class='ethics'><b>ETHICS:</b> uchunguzi huu ulifanyika "
        "kwenye mifumo YAKO tu. Kuchunguza port za mtu mwingine bila "
        "ruhusa ni kosa la sheria.</div>"
        "<p class='lebo'>Imetengenezwa na CyberToolkit (P7)</p>"
        "</body></html>\n"
    ) % (host, host, host, sasa, len(zote), len(wazi),
         len(zote) - len(wazi), "".join(mistari))
    with open(njia, "w", encoding="utf-8") as f:
        f.write(html)
    return njia


def menyu():
    print("=" * 54)
    print("  CYBER TOOLKIT - MENYU  (ethics: mifumo YAKO tu)")
    print("=" * 54)
    try:
        while True:
            print("""
  1 - Hash ya neno
  2 - Siri (ficha/fungua)
  3 - Tengeneza nenosiri
  4 - Kagua nenosiri
  5 - Ports
  6 - IP
  0 - TOKA
""")
            chaguo = input("  chagua: ").strip()
            if chaguo == "0":
                print("Kwaheri!")
                return 0
            elif chaguo == "1":
                main(["hash", input("  neno: ")])
            elif chaguo == "2":
                hali = input("  ficha/fungua: ").strip().lower()
                fumbo = input("  funguo: ")
                maandishi = input("  maandishi: ")
                if hali == "fungua":
                    main(["siri", "--fumbo", fumbo, "--fungua", maandishi])
                else:
                    main(["siri", "--fumbo", fumbo, "--andika",
                          maandishi])
            elif chaguo == "3":
                n = input("  urefu [16]: ").strip() or "16"
                main(["tengeneza", "-n", n])
            elif chaguo == "4":
                main(["imarisha", input("  nenosiri: ")])
            elif chaguo == "5":
                host = input("  host [127.0.0.1]: ").strip() \
                    or "127.0.0.1"
                a = input("  ports [mf. 22,80 au tupu=zote]: ").strip()
                amri = ["ports", host]
                if a:
                    amri += ["--a", a]
                main(amri)
            elif chaguo == "6":
                ipk = input("  IP [tupu = yangu]: ").strip()
                main(["ip"] + ([ipk] if ipk else []))
            else:
                print("  Chaguo si sahihi, jaribu tena")
    except (EOFError, KeyboardInterrupt):
        print("\nKwaheri!")
        return 0


def maswali(mambo=None):
    m = argparse.ArgumentParser(
        prog="cyber.py",
        description="CyberToolkit - zana 8 za usalama (offline, ethics kwanza)")
    sub = m.add_subparsers(dest="amri", required=True)

    p = sub.add_parser("hash", help="SHA hash ya neno AU file + thibitisha")
    p.add_argument("maneno", nargs="?", help="neno la kutaka hash")
    p.add_argument("--mzigo", help="njia ya file")
    p.add_argument("--a", default="sha256",
                   choices=["sha256", "sha512", "sha1", "sha3_256"],
                   help="algorithimu")
    p.add_argument("--thibitisha", help="linganisha na hii hash")

    p = sub.add_parser("siri", help="Ficha/fungua maandishi (XOR+base64)")
    p.add_argument("--fumbo", required=True, help="funguo ya siri")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--andika", help="maandishi ya kuficha")
    g.add_argument("--fungua", help="base64 ya kufungua")

    p = sub.add_parser("tengeneza", help="Tengeneza nenosiri imara")
    p.add_argument("-n", "--urefu", type=int, default=16)

    p = sub.add_parser("imarisha", help="Kagua nguvu ya nenosiri")
    p.add_argument("nenosiri")

    p = sub.add_parser("ports", help="TCP scan ya ports (mifumo yako tu!)")
    p.add_argument("host", nargs="?", default="127.0.0.1")
    p.add_argument("--a", help="orodha: 22,80,443")
    p.add_argument("--mzigo", help="mzigo: 1-1024")
    p.add_argument("--muda", type=float, default=0.5)

    p = sub.add_parser("ip", help="Chambua IP: private/loopback/public")
    p.add_argument("kielelezo", nargs="?", help="IP ya kuchambua")

    sub.add_parser("menyu", help="Menyu ya kibonzo (interactive)")

    p = sub.add_parser("ripoti", help="Uchunguza ports + hifadhi ripoti HTML")
    p.add_argument("host", nargs="?", default="127.0.0.1")
    p.add_argument("--a", help="orodha: 22,80,443")
    p.add_argument("--mzigo", help="mzigo: 1-1024")
    p.add_argument("--muda", type=float, default=0.5)
    p.add_argument("-o", "--njia", default="ripoti-cyber.html",
                   help="file ya HTML ya kuhifadhi")
    p.add_argument("--fungua", action="store_true",
                   help="fungua ripoti kwenye browser")
    return m


def endesha(mambo):
    if mambo.amri == "hash":
        if mambo.mzigo:
            dokezo = hash_file(mambo.mzigo, mambo.a)
            msingi = "%s (%s)" % (mambo.mzigo, mambo.a)
        elif mambo.maneno is not None:
            dokezo = hesabu_hash(mambo.maneno.encode("utf-8"), mambo.a)
            msingi = mambo.maneno
        else:
            print("Toa neno AU --mzigo")
            return 1
        print("%s" % dokezo)
        if mambo.thibitisha:
            sawa = hmac.compare_digest(dokezo, mambo.thibitisha.lower())
            print("THIBITISHO: %s" % ("SAWA" if sawa else "TOFAUTI!"))
            return 0 if sawa else 1
        print("msingi: %s | algorithimu: %s" % (msingi, mambo.a))
        return 0

    if mambo.amri == "siri":
        if mambo.andika is not None:
            print(siri_mandishi(mambo.andika, mambo.fumbo))
        else:
            print(fungua_mandishi(mambo.fungua, mambo.fumbo))
        return 0

    if mambo.amri == "tengeneza":
        neno = tengeneza_nenosiri(mambo.urefu)
        print(neno)
        s = imarisha_nenosiri(neno)
        print("alama: %s/6 | hukumu: %s | entropy: %.1f bits" % (
            s["alama"], s["hukumu"], s["entropy"]))
        return 0

    if mambo.amri == "imarisha":
        s = imarisha_nenosiri(mambo.nenosiri)
        print("hukumu: %s (alama %s/6)" % (s["hukumu"], s["alama"]))
        print("entropy: %.1f bits" % s["entropy"])
        for p in s["mapendekezo"]:
            print("  - %s" % p)
        return 0

    if mambo.amri == "menyu":
        return menyu()

    if mambo.amri == "ports":
        porta = jenga_porta(mambo.a, mambo.mzigo)
        print("Inachunguza %s... (ports %d, muda %ss)" % (
            mambo.host, len(porta), mambo.muda))
        zazi = chunguza_ports(mambo.host, porta, mambo.muda)
        if not zazi:
            print("Hakuna port iliyofunguliwa iliyopatikana")
            return 0
        for p in zazi:
            jina = PORTA_ZINAZOJULIKANA.get(p, "?")
            print("  WAZI  %s/%s" % (p, jina))
        print("Jumla wazi: %d" % len(zazi))
        return 0

    if mambo.amri == "ripoti":
        porta = jenga_porta(mambo.a, mambo.mzigo)
        print("Inachunguza %s... (ports %d)" % (mambo.host, len(porta)))
        zazi = chunguza_ports(mambo.host, porta, mambo.muda)
        njia = andika_ripoti(mambo.host, zazi, porta, mambo.njia)
        print("Ripoti IMEHIFADHIWA: %s (%d wazi kati ya %d)" % (
            njia, len(zazi), len(porta)))
        if mambo.fungua:
            webbrowser.open("file://" + os.path.abspath(njia))
        return 0

    if mambo.amri == "ip":
        if mambo.kielelezo:
            sifa = ip_funguo(mambo.kielelezo)
            print("%s -> version %s | %s" % (
                sifa["ip"], sifa["version"],
                "PRIVATE" if sifa["private"] else "PUBLIC"))
            for k in ("loopback", "link_local", "multicast",
                      "global", "reserved"):
                if sifa[k]:
                    print("  + %s" % k)
            return 0
        try:
            yangu = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            yangu = "127.0.0.1"
        print("IP yangu: %s" % yangu)
        sifa = ip_funguo(yangu)
        print("hali: %s" % ("PRIVATE" if sifa["private"] else "PUBLIC"))
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
