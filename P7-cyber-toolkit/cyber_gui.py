import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import cyber


class CyberGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CyberToolkit GUI - P7 (ethics: mifumo YAKO tu)")
        self.geometry("760x560")
        self.minsize(680, 480)
        kadi = ttk.Notebook(self)
        kadi.pack(fill="both", expand=True, padx=8, pady=8)

        self.matokeo_safari = queue.Queue()

        self.tab_hash(kadi)
        self.tab_siri(kadi)
        self.tab_nenosiri(kadi)
        self.tab_ports(kadi)
        self.tab_ip(kadi)

    def sehemu_mstari(self, mzazi, lebo, thamani=""):
        fremu = ttk.Frame(mzazi)
        fremu.pack(fill="x", padx=10, pady=4)
        ttk.Label(fremu, text=lebo, width=16).pack(side="left")
        k = ttk.Entry(fremu)
        k.insert(0, thamani)
        k.pack(side="left", fill="x", expand=True)
        return k

    def sehemu_matokeo(self, mzazi):
        fremu = ttk.Frame(mzazi)
        fremu.pack(fill="both", expand=True, padx=10, pady=6)
        m = tk.Text(fremu, height=12, wrap="word", state="normal")
        m.pack(fill="both", expand=True)
        return m

    def tab_hash(self, kadi):
        t = ttk.Frame(kadi)
        kadi.add(t, text="Hash")
        self.h_maneno = self.sehemu_mstari(t, "Neno:")
        self.h_aina = ttk.Combobox(t, values=[
            "sha256", "sha512", "sha1", "sha3_256"], state="readonly")
        self.h_aina.current(0)
        self.h_thibitisha = self.sehemu_mstari(t, "Thibitisha:")
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=6)
        ttk.Button(fremu, text="Hash neno",
                   command=self.fanya_hash).pack(side="left", padx=4)
        ttk.Button(fremu, text="Hash file...",
                   command=self.hash_file).pack(side="left", padx=4)
        ttk.Button(fremu, text="Thibitisha",
                   command=self.thibitisha_hash).pack(side="left", padx=4)
        self.h_matokeo = self.sehemu_matokeo(t)

    def fanya_hash(self):
        neno = self.h_maneno.get()
        if not neno:
            return
        dokezo = cyber.hesabu_hash(neno.encode("utf-8"),
                                   self.h_aina.get())
        self.h_matokeo.delete("1.0", "end")
        self.h_matokeo.insert("end", dokezo + "\n")

    def hash_file(self):
        njia = filedialog.askopenfilename(title="Chagua file")
        if not njia:
            return
        try:
            dokezo = cyber.hash_file(njia, self.h_aina.get())
        except OSError as e:
            messagebox.showerror("Hitilafu", str(e))
            return
        self.h_matokeo.delete("1.0", "end")
        self.h_matokeo.insert("end", njia + "\n" + dokezo + "\n")

    def thibitisha_hash(self):
        asilia = self.h_matokeo.get("1.0", "end").split()[:1]
        lengo = self.h_thibitisha.get().strip().lower()
        if not asilia or not lengo:
            messagebox.showwarning("Onyo",
                                   "Hash ya kwanza na yenye thibitisha "
                                   "zinahitajika")
            return
        import hmac as _hmac
        sawa = _hmac.compare_digest(asilia[0], lengo)
        self.h_matokeo.insert("end",
                              "THIBITISHO: %s\n" % ("SAWA" if sawa
                                                    else "TOFAUTI!"))

    def tab_siri(self, kadi):
        t = ttk.Frame(kadi)
        kadi.add(t, text="Siri")
        self.s_hali = tk.StringVar(value="ficha")
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=4)
        ttk.Radiobutton(fremu, text="Ficha", variable=self.s_hali,
                        value="ficha").pack(side="left", padx=6)
        ttk.Radiobutton(fremu, text="Fungua", variable=self.s_hali,
                        value="fungua").pack(side="left", padx=6)
        self.s_funguo = self.sehemu_mstari(t, "Funguo:")
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=2)
        ttk.Label(fremu, text="Maandishi:").pack(anchor="w")
        self.s_ndani = tk.Text(t, height=5, wrap="word")
        self.s_ndani.pack(fill="x", padx=10)
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=6)
        ttk.Button(fremu, text="Fanya",
                   command=self.fanya_siri).pack(side="left", padx=4)
        self.s_matokeo = self.sehemu_matokeo(t)

    def fanya_siri(self):
        fumbo = self.s_funguo.get()
        ndani = self.s_ndani.get("1.0", "end").rstrip("\n")
        try:
            if self.s_hali.get() == "ficha":
                toa = cyber.siri_mandishi(ndani, fumbo)
            else:
                toa = cyber.fungua_mandishi(ndani, fumbo)
        except ValueError as e:
            messagebox.showerror("Hitilafu", str(e))
            return
        self.s_matokeo.delete("1.0", "end")
        self.s_matokeo.insert("end", toa + "\n")

    def tab_nenosiri(self, kadi):
        t = ttk.Frame(kadi)
        kadi.add(t, text="Nenosiri")
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=6)
        ttk.Label(fremu, text="Urefu:").pack(side="left")
        self.n_urefu = tk.Spinbox(fremu, from_=4, to=64, width=5)
        self.n_urefu.delete(0, "end")
        self.n_urefu.insert(0, "16")
        self.n_urefu.pack(side="left", padx=6)
        ttk.Button(fremu, text="Tengeneza",
                   command=self.tengeneza_neno).pack(side="left", padx=10)
        self.n_jaribu = self.sehemu_mstari(t, "Kagua neno:")
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=4)
        ttk.Button(fremu, text="Kagua nguvu",
                   command=self.kagua_neno).pack(side="left", padx=4)
        self.n_matokeo = self.sehemu_matokeo(t)

    def tengeneza_neno(self):
        try:
            urefu = int(self.n_urefu.get())
            neno = cyber.tengeneza_nenosiri(urefu)
        except ValueError as e:
            messagebox.showerror("Hitilafu", str(e))
            return
        self.n_jaribu.delete(0, "end")
        self.n_jaribu.insert(0, neno)
        self.onyesha_kagua(neno)

    def kagua_neno(self):
        neno = self.n_jaribu.get()
        if not neno:
            return
        self.onyesha_kagua(neno)

    def onyesha_kagua(self, neno):
        s = cyber.imarisha_nenosiri(neno)
        self.n_matokeo.delete("1.0", "end")
        self.n_matokeo.insert("end", "hukumu: %s (alama %s/6)\n" % (
            s["hukumu"], s["alama"]))
        self.n_matokeo.insert("end", "entropy: %.1f bits\n" % s["entropy"])
        for p in s["mapendekezo"]:
            self.n_matokeo.insert("end", "  - %s\n" % p)

    def tab_ports(self, kadi):
        t = ttk.Frame(kadi)
        kadi.add(t, text="Ports")
        self.p_host = self.sehemu_mstari(t, "Host:", "127.0.0.1")
        self.p_ports = self.sehemu_mstari(t, "Ports:", "22,80,443,5000")
        self.p_muda = self.sehemu_mstari(t, "Muda (s):", "0.5")
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=6)
        self.p_kitufe = ttk.Button(fremu, text="Chunguza",
                                   command=self.anza_chunguza)
        self.p_kitufe.pack(side="left", padx=4)
        ttk.Label(fremu, text="Tumia kwenye mifumo YAKO tu!").pack(
            side="left", padx=8)
        self.p_matokeo = self.sehemu_matokeo(t)

    def anza_chunguza(self):
        host = self.p_host.get().strip()
        maandishi = self.p_ports.get().strip()
        try:
            muda = float(self.p_muda.get())
            if maandishi:
                if "-" in maandishi:
                    mwanzo, mwisho = maandishi.split("-")
                    porta = list(range(int(mwanzo), int(mwisho) + 1))
                else:
                    porta = [int(x) for x in maandishi.split(",")
                             if x.strip()]
            else:
                porta = list(cyber.PORTA_ZINAZOJULIKANA)
            if not porta or len(porta) > 5000:
                raise ValueError("Ports 1-5000 tu")
        except ValueError as e:
            messagebox.showerror("Hitilafu", str(e))
            return
        self.p_matokeo.delete("1.0", "end")
        self.p_matokeo.insert("end", "Inachunguza %s (%d ports)...\n" % (
            host, len(porta)))
        self.p_kitufe.state(["disabled"])
        self.matokeo_safari = queue.Queue()

        def kazi():
            r = cyber.chunguza_ports(host, porta, muda)
            self.matokeo_safari.put(r)

        threading.Thread(target=kazi, daemon=True).start()
        self.after(200, self.dakia_matokeo)

    def dakia_matokeo(self):
        try:
            r = self.matokeo_safari.get_nowait()
        except queue.Empty:
            self.after(200, self.dakia_matokeo)
            return
        if not r:
            self.p_matokeo.insert("end",
                                  "Hakuna port iliyofunguliwa\n")
        for p in r:
            jina = cyber.PORTA_ZINAZOJULIKANA.get(p, "?")
            self.p_matokeo.insert("end", "  WAZI  %s/%s\n" % (p, jina))
        self.p_matokeo.insert("end", "Jumla wazi: %d\n" % len(r))
        self.p_kitufe.state(["!disabled"])

    def tab_ip(self, kadi):
        t = ttk.Frame(kadi)
        kadi.add(t, text="IP")
        self.i_ip = self.sehemu_mstari(t, "IP (bo tupu = yangu):")
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=6)
        ttk.Button(fremu, text="Chambua",
                   command=self.chambua_ip).pack(side="left", padx=4)
        ttk.Button(fremu, text="IP yangu",
                   command=self.ip_yangu).pack(side="left", padx=4)
        self.i_matokeo = self.sehemu_matokeo(t)

    def chambua_ip(self):
        mwako = self.i_ip.get().strip()
        if not mwako:
            self.ip_yangu()
            return
        try:
            sifa = cyber.ip_funguo(mwako)
        except ValueError as e:
            messagebox.showerror("Hitilafu", str(e))
            return
        self.i_matokeo.delete("1.0", "end")
        self.i_matokeo.insert("end", "%s -> version %s | %s\n" % (
            sifa["ip"], sifa["version"],
            "PRIVATE" if sifa["private"] else "PUBLIC"))
        for k in ("loopback", "link_local", "multicast", "global",
                  "reserved"):
            if sifa[k]:
                self.i_matokeo.insert("end", "  + %s\n" % k)

    def ip_yangu(self):
        import socket
        try:
            yangu = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            yangu = "127.0.0.1"
        self.i_ip.delete(0, "end")
        self.i_ip.insert(0, yangu)
        self.chambua_ip()


if __name__ == "__main__":
    CyberGUI().mainloop()
