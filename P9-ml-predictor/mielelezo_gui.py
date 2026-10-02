import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

import mielelezo as m


class MielelezoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mielelezo GUI - P9 (ML ya offline, sklearn)")
        self.geometry("740x540")
        self.minsize(640, 460)
        self.kazi_safari = queue.Queue()
        kadi = ttk.Notebook(self)
        kadi.pack(fill="both", expand=True, padx=8, pady=8)
        self.tab_tabiri(kadi)
        self.tab_fundisha(kadi)
        self.tab_data(kadi)

    def onyesha_matokeo(self, mzazi, urefu=10):
        t = tk.Text(mzazi, height=urefu, wrap="word", state="normal")
        t.pack(fill="both", expand=True, padx=10, pady=6)
        return t

    def tab_tabiri(self, kadi):
        t = ttk.Frame(kadi)
        kadi.add(t, text="Tabiri")
        ttk.Label(t, text="Andika ujumbe (SMS/WhatsApp):").pack(
            anchor="w", padx=10, pady=(10, 2))
        self.t_ndani = tk.Text(t, height=4, wrap="word")
        self.t_ndani.pack(fill="x", padx=10)
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=6)
        ttk.Button(fremu, text="Tabiri",
                   command=self.tabiri).pack(side="left", padx=4)
        ttk.Button(fremu, text="Futa",
                   command=lambda: self.t_ndani.delete("1.0", "end")
                   ).pack(side="left", padx=4)
        ttk.Label(fremu,
                  text="Mfano: Umeshinda zawadi tuma namba ya siri"
                  ).pack(side="left", padx=8)
        self.t_alama = ttk.Label(t, text="—", font=("Segoe UI", 22, "bold"))
        self.t_alama.pack(pady=(8, 0))
        self.t_uwezo = ttk.Label(t, text="")
        self.t_uwezo.pack()
        self.t_maelezo = ttk.Label(
            t, text="Fundisha model kwanza (tab ya Fundisha) ikiwa "
                    "haijafundishwa.", wraplength=600)
        self.t_maelezo.pack(pady=8)

    def tabiri(self):
        ujumbe = self.t_ndani.get("1.0", "end").strip()
        if not ujumbe:
            messagebox.showwarning("Onyo", "Andika ujumbe kwanza")
            return
        try:
            r = m.angalia(ujumbe)
        except FileNotFoundError:
            self.t_alama.config(text="??")
            self.t_maelezo.config(
                text="Model haipo - bonyeza 'Fundisha model' kwanza.")
            return
        aina = r["aina"].upper()
        rangi = "#c0392b" if aina == "SPAM" else "#27ae60"
        self.t_alama.config(text=aina, foreground=rangi)
        self.t_uwezo.config(text="uwezo: %.1f%%" % r["uwezo"])
        if aina == "SPAM":
            dokezo = ("Onyo: inaonekana SPAM. Usibonyeze viungo wala "
                      "tume namba ya siri.")
        else:
            dokezo = ("Inaonekana ujumbe halisi (HAM). Sawa na ujumbe "
                      "wa kawaida.")
        if r["uwezo"] < 80:
            dokezo += " (Uwezo ni chini ya 80% - kuwa makini!)"
        self.t_maelezo.config(text=dokezo)

    def tab_fundisha(self, kadi):
        t = ttk.Frame(kadi)
        kadi.add(t, text="Fundisha")
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=8)
        self.f_kitufe = ttk.Button(fremu, text="Fundisha model",
                                   command=self.anza_fundisha)
        self.f_kitufe.pack(side="left", padx=4)
        ttk.Button(fremu, text="Thibitisha",
                   command=self.thibitisha).pack(side="left", padx=4)
        ttk.Label(fremu,
                  text="Inachukua sekunde chache...").pack(side="left",
                                                           padx=8)
        self.f_matokeo = self.onyesha_matokeo(t, 16)

    def anza_fundisha(self):
        self.f_kitufe.state(["disabled"])
        self.f_matokeo.delete("1.0", "end")
        self.f_matokeo.insert("end", "Inafundisha...\n")
        self.kazi_safari = queue.Queue()

        def kazi():
            try:
                d = m.fundisha()
                self.kazi_safari.put(("ok", d))
            except Exception as e:
                self.kazi_safari.put(("hitilafu", str(e)))

        threading.Thread(target=kazi, daemon=True).start()
        self.after(200, self.dakia_fundisha)

    def dakia_fundisha(self):
        try:
            aina, thamani = self.kazi_safari.get_nowait()
        except queue.Empty:
            self.after(200, self.dakia_fundisha)
            return
        self.f_kitufe.state(["!disabled"])
        self.f_matokeo.delete("1.0", "end")
        if aina == "hitilafu":
            messagebox.showerror("Hitilafu", thamani)
            return
        d = thamani
        self.f_matokeo.insert(
            "end", "IMEFUNDISHWA: mifano %d (mafunzo %d / mtihani %d)\n"
            % (d["jumla"], d["mafunzo"], d["mtihani"]))
        self.f_matokeo.insert("end",
                              "Usahihi: %.1f%%\n" % (d["usahihi"] * 100))
        self.f_matokeo.insert("end", "Maneno: %d\n\n" % d["maneno"])
        self.f_matokeo.insert("end", d["ripoti"])
        self.f_matokeo.insert(
            "end", "\nMatrix (nyaya=halisi, safu=[[ham,spam]])\n")
        for mstari in d["matrix"]:
            self.f_matokeo.insert("end", "  %s\n" % mstari)
        self.f_matokeo.insert("end", "\nModel: %s" % m.MODEL)

    def thibitisha(self):
        try:
            d = m.thibitisha()
        except FileNotFoundError:
            messagebox.showerror("Hitilafu",
                                 "Model haipo - fundisha kwanza")
            return
        self.f_matokeo.delete("1.0", "end")
        self.f_matokeo.insert("end", "Usahihi: %.1f%%\n\n"
                              % (d["usahihi"] * 100))
        self.f_matokeo.insert("end", d["ripoti"])

    def tab_data(self, kadi):
        t = ttk.Frame(kadi)
        kadi.add(t, text="Data")
        fremu = ttk.Frame(t)
        fremu.pack(fill="x", padx=10, pady=8)
        ttk.Button(fremu, text="Onyesha data (sms.csv)",
                   command=self.onyesha_data).pack(side="left", padx=4)
        self.d_matokeo = self.onyesha_matokeo(t, 16)

    def onyesha_data(self):
        try:
            ujumbe, lebo = m.pakua_data()
        except (OSError, ValueError) as e:
            messagebox.showerror("Hitilafu", str(e))
            return
        idadi = {"spam": lebo.count("spam"), "ham": lebo.count("ham")}
        self.d_matokeo.delete("1.0", "end")
        self.d_matokeo.insert("end", "Jumla ya mifano: %d\n" % len(ujumbe))
        self.d_matokeo.insert("end", "  spam: %d\n" % idadi["spam"])
        self.d_matokeo.insert("end", "  ham:  %d\n\n" % idadi["ham"])
        self.d_matokeo.insert("end", "Mifano (3 kila aina):\n")
        kwa = {"spam": 0, "ham": 0}
        for u, l in zip(ujumbe, lebo):
            if kwa[l] < 3:
                self.d_matokeo.insert("end", "  [%s] %s\n" % (l, u))
                kwa[l] += 1


if __name__ == "__main__":
    MielelezoGUI().mainloop()
