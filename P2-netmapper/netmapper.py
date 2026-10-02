# ============================================================
# P2 - NETMAPPER v1.1: Ramani ya Mtandao (IP Sweep + Port Scan)
# Endesha: python netmapper.py [--subnet 192.168.1.0/24] [--ports 80,445]
# ETHICS: Tumia tu kwenye mtandao WAKO au uliopewa ruhusa.
# ============================================================
import socket
import sys
import time
import re
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

SCAN_PORTS = [21, 22, 23, 80, 135, 139, 443, 445, 3389, 8080]
TIMEOUT = 0.5
MAX_WORKERS = 64

SERVICE = {
    21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 135: "MSRPC", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 3389: "RDP", 8080: "HTTP-ALT",
}
RISKY = {23: "TELNET", 21: "FTP", 3389: "RDP", 445: "SMB"}


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


def get_subnet():
    return ".".join(get_local_ip().split(".")[:3]) + ".0/24"


def check_host(ip, ports):
    """Rudisha (ip, host, [ports], ms) ama None"""
    open_ports, ms = [], None
    t0 = time.time()
    for p in ports:
        try:
            with socket.create_connection((ip, p), timeout=TIMEOUT):
                open_ports.append(p)
                if ms is None:
                    ms = int((time.time() - t0) * 1000)
        except (socket.timeout, ConnectionRefusedError, OSError):
            pass
    if not open_ports:
        return None
    try:
        host = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        host = "-"
    return (ip, host, open_ports, ms or 0)


def scan(subnet, ports):
    results = []
    ips = [str(h) for h in ipaddress.IPv4Network(subnet, strict=False).hosts()]
    print(f"Inachunguza {len(ips)} IP kwenye {subnet} ...")
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(check_host, ip, ports): ip for ip in ips}
        for f in as_completed(futures):
            r = f.result()
            if r:
                results.append(r)
                svcs = ",".join(SERVICE.get(p, str(p)) for p in r[2])
                print(f"  [HAI] {r[0]:<16} {svcs:<40} {r[3]}ms")
    return sorted(results), round(time.time() - t0, 1)


def get_arp():
    """Rudisha {ip: mac} kutoka arp -a (baa ya kufanya scan)"""
    arp = {}
    try:
        out = subprocess.run(["arp", "-a"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            m = re.match(r"\s*(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})", line)
            if m:
                arp[m.group(1)] = m.group(2)
    except Exception:
        pass
    return arp


def security_mark(open_ports):
    hit = [name for p, name in RISKY.items() if p in open_ports]
    if "TELNET" in hit or "FTP" in hit:
        return "#e74c3c", "HATARI: " + ", ".join(hit) + " wazi (huduma ya zamani)"
    if hit:
        return "#f39c12", "ZINGATIA: " + ", ".join(hit) + " wazi"
    return "#27ae60", "Hakuna huduma hatari iliyopatikana"


def write_report(results, subnet, dt, ports, arp, fname="netmap.html"):
    rows = ""
    hatari = 0
    for ip, host, ops, ms in results:
        col, note = security_mark(ops)
        if col != "#27ae60":
            hatari += 1
        svc = ", ".join(f"{p} ({SERVICE.get(p, '?')})" for p in ops)
        mac = arp.get(ip, "-")
        rows += f"""
    <tr><td>{ip}</td><td style="font-family:monospace">{mac}</td><td>{host}</td>
      <td>{svc}</td><td>{ms} ms</td>
      <td style="color:{col};font-weight:700">&#9679;</td><td>{note}</td></tr>"""

    total = len(list(ipaddress.IPv4Network(subnet, strict=False).hosts()))
    legend = "".join(
        f"<tr><td>{p}</td><td>{SERVICE[p]}</td></tr>"
        for p in sorted(SERVICE) if p in ports
    )
    html = f"""<!DOCTYPE html><html lang="sw"><head><meta charset="UTF-8">
<title>NETMAPPER</title><style>
 body{{font-family:'Segoe UI',Arial;background:#f4f6f9;margin:0;padding:24px;color:#2c3e50}}
 .wrap{{max-width:1050px;margin:auto}}
 h1{{background:linear-gradient(135deg,#16a085,#2c3e50);color:#fff;padding:20px 26px;border-radius:10px;margin:0 0 6px}}
 .sub{{color:#7f8c8d;margin-bottom:18px}}
 .stats{{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:16px}}
 .pill{{background:#fff;border-radius:10px;padding:10px 18px;box-shadow:0 2px 6px rgba(0,0,0,.08);font-weight:700}}
 table{{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 6px rgba(0,0,0,.08);margin-bottom:16px}}
 th{{background:#2c3e50;color:#fff;padding:9px;text-align:left;font-size:13px}}
 td{{padding:8px 9px;border-bottom:1px solid #ecf0f1;font-size:14px}}
 tr:nth-child(even) td{{background:#f9f9f9}}
 .warn{{background:#fff3cd;border-left:6px solid #f39c12;padding:10px 14px;border-radius:8px;font-size:13px;margin-bottom:10px}}
 .info{{background:#e8f6f3;border-left:6px solid #16a085;padding:10px 14px;border-radius:8px;font-size:13px}}
 h3{{margin:18px 0 8px}}
 footer{{text-align:center;color:#95a5a6;font-size:12px;margin-top:16px}}
</style></head><body><div class="wrap">
<h1>&#128506; NETMAPPER v1.1</h1>
<div class="sub">{subnet} &mdash; iliyotengenezwa: {time.strftime('%d/%m/%Y %H:%M')}</div>
<div class="stats">
  <div class="pill">IP zilizopigwa: {total}</div>
  <div class="pill" style="color:#27ae60">Zilizojibu: {len(results)}</div>
  <div class="pill" style="color:{'#e74c3c' if hatari else '#27ae60'}">Zenye onyo: {hatari}</div>
  <div class="pill">Muda: {dt}s</div>
</div>

<div class="warn">&#9888; <b>MUHTASARI WA MENEJA:</b> Vifaa {len(results)} vipo mtandaoni;
{hatari} vina huduma zinazohitaji ukaguzi (RDP/SMB/FTP/TELNET wazi).
Angalia jedwali hapa chini.</div>

<table><tr><th>IP</th><th>MAC</th><th>Jina (hostname)</th><th>Huduma (port + jina)</th>
<th>Latency</th><th>Hali</th><th>Maelezo ya usalama</th></tr>{rows}</table>

<div class="info"><b>MAANA YA PORTI (legend):</b>
<table style="width:auto;margin-top:6px"><tr><th style="padding:5px">Porti</th><th style="padding:5px">Huduma</th></tr>{legend}</table>
</div>

<div class="warn"><b>ETHICS:</b> Chombo cha ukaguzi - tumia tu kwenye mtandao wako
au uliopewa RUHUSA. Kutafuta mtandao wa mwingeni ni kinyume cha sheria.</div>

<footer>NETMAPPER v1.1 &mdash; PORTFOLIO P2 &mdash; Python socket + ThreadPool + ARP</footer>
</div></body></html>"""
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    return fname


if __name__ == "__main__":
    import subprocess  # kwa arp -a
    ports, subnet = SCAN_PORTS, get_subnet()
    if "--ports" in sys.argv:
        ports = [int(p) for p in sys.argv[sys.argv.index("--ports") + 1].split(",")]
    if "--subnet" in sys.argv:
        subnet = sys.argv[sys.argv.index("--subnet") + 1]

    results, dt = scan(subnet, ports)
    arp = get_arp()
    print(f"\nImekamilika: {len(results)} zilizojibu katika {dt}s (MAC kutoka ARP: {len(arp)})")
    out = write_report(results, subnet, dt, ports, arp)
    print(f"Ripoti: {out}")
    try:
        import webbrowser
        webbrowser.open(out)
    except Exception:
        pass
