const miradi = [
  {
    id: "P1",
    jina: "SysReport",
    hali: "done",
    maelezo: "Ripoti ya PC (CPU, RAM, disk, programu) kwa PowerShell + HTML + ratiba ya kila siku (Task Scheduler).",
    tekh: ["PowerShell", "CIM", "HTML", "Task Scheduler"],
    kiungo: "../P1-sysreport/report.html",
    kiungo_maandishi: "Fungua ripoti (report.html)",
    maelezo_zaidi: "Endesha: powershell -File sysreport.ps1 (ikiwa report.html haipo bado)",
  },
  {
    id: "P2",
    jina: "NetMapper",
    hali: "done",
    maelezo: "Ramani ya mtandao: IP zilizo hai, milango (ports), alama za usalama, MAC/ARP - HTML dashboard.",
    tekh: ["Python", "socket", "ThreadPool", "ARP"],
    kiungo: "../P2-netmapper/netmap.html",
    kiungo_maandishi: "Fungua dashboard (netmap.html)",
    maelezo_zaidi: "Endesha: python netmap.py (inatengeneza ripoti mpya kila unapoitumia)",
  },
  {
    id: "P3",
    jina: "Mkopo CLI Pro",
    hali: "done",
    maelezo: "Mfumo wa mikopo: CRUD kamili, riba flat/reducing, SQL queries, CSV export, logs, tests 18+.",
    tekh: ["Python", "SQLite", "argparse", "pytest"],
    kiungo: "../P3-mkopo-cli/",
    kiungo_maandishi: "Fungua folda ya mradi",
    maelezo_zaidi: "Endesha: cd P3-mkopo-cli; python main.py menyu",
  },
  {
    id: "P4",
    jina: "Portfolio Website",
    hali: "done",
    maelezo: "Tovuti hii mwenyewe: HTML + CSS + JS (responsive, kuratibu miradi na vichujio).",
    tekh: ["HTML", "CSS Grid", "JavaScript", "DOM"],
    kiungo: "",
    kiungo_maandishi: "",
    maelezo_zaidi: "Umekomboa! Faili: index.html, style.css, script.js",
  },
  {
    id: "P5",
    jina: "Database Design",
    hali: "done",
    maelezo: "Muundo wa database ya kweli: ERD, tables, constraints, VIEW, TRIGGER + backup (SQLite).",
    tekh: ["SQL", "SQLite", "ERD", "TRIGGER"],
    kiungo: "../P5-database-design/erd.html",
    kiungo_maandishi: "Fungua ERD (erd.html)",
    maelezo_zaidi: "Endesha: cd P5-database-design; python fanya.py (queries, trigger, backup)",
  },
  {
    id: "P6",
    jina: "Benki App v2",
    hali: "done",
    maelezo: "Mfumo wa benki kwenye web: login + CSRF, majukumu 3 (admin/mpokeaji/mhasibu), wateja, mikopo, badilisha nenosiri (tests 14).",
    tekh: ["Flask", "Auth", "CSRF", "SQLite"],
    kiungo: "../P6-benki-app/",
    kiungo_maandishi: "Fungua folda ya mradi",
    maelezo_zaidi: "Endesha: cd P6-benki-app; python app.py kisha http://localhost:5000 (admin/benki123)",
  },
  {
    id: "P7",
    jina: "CyberToolkit",
    hali: "done",
    maelezo: "Zana 8 za usalama: hash, siri (HMAC), scanner ya milango, hardening + GUI ya Tkinter (tests 15).",
    tekh: ["Python", "hashlib", "sockets", "Tkinter"],
    kiungo: "../P7-cyber-toolkit/",
    kiungo_maandishi: "Fungua folda ya mradi",
    maelezo_zaidi: "Endesha: cd P7-cyber-toolkit; python cyber.py menyu",
  },
  {
    id: "P8",
    jina: "Docker/Compose",
    hali: "done",
    maelezo: "Benki App kwenye containers: image + compose + volume ya data (persistent) + healthcheck (tests 6).",
    tekh: ["Dockerfile", "Compose", "Linux"],
    kiungo: "../P8-docker-benki/",
    kiungo_maandishi: "Fungua folda ya mradi",
    maelezo_zaidi: "Endesha: cd P8-docker-benki; docker compose up -d --build",
  },
  {
    id: "P9",
    jina: "Mielelezo (Spam Predictor)",
    hali: "done",
    maelezo: "ML ya offline: TF-IDF + Naive Bayes, train/test split, metriki (94.7%), model iliyohifadhiwa (tests 9).",
    tekh: ["scikit-learn", "TF-IDF", "Naive Bayes", "pytest"],
    kiungo: "../P9-ml-predictor/",
    kiungo_maandishi: "Fungua folda ya mradi",
    maelezo_zaidi: "Endesha: cd P9-ml-predictor; python mielelezo.py fundisha (au python mielelezo_gui.py - GUI)",
  },
  {
    id: "P10",
    jina: "Benki 360 (Django)",
    hali: "done",
    maelezo: "Mradi mkuu #1: mfumo kamili wa benki kwa Django 6 - ORM, majukumu 3, CSRF, CASCADE, admin ya Kiswahili (tests 19).",
    tekh: ["Django", "ORM", "Auth/CSRF", "pytest-django"],
    kiungo: "../P10-django-benki360/",
    kiungo_maandishi: "Fungua folda ya mradi",
    maelezo_zaidi: "Endesha: cd P10-django-benki360; python manage.py runserver (admin/benki123)",
  },
  {
    id: "P11",
    jina: "Ofisi 360 (Django)",
    hali: "done",
    maelezo: "Mradi mkuu #2 (PPRA): daftari la barua (faili+namba), workflow ya maombi (rasimu→idhini/kataa), audit trail kwa signals, ripoti CSV (tests 20).",
    tekh: ["Django", "CBV", "Signals", "File upload"],
    kiungo: "../P11-ofisi-django/",
    kiungo_maandishi: "Fungua folda ya mradi",
    maelezo_zaidi: "Endesha: cd P11-ofisi-django; python manage.py runserver (admin/ofisi123, neema/meneja123)",
  },
  {
    id: "P12",
    jina: "Duka la Kwanza (E-commerce)",
    hali: "done",
    maelezo: "Mradi mkuu #3: duka la mtandaoni - M2M lebo, kikapu (context processor), checkout atomic, snapshot ya bei, Update/DeleteView (tests 24).",
    tekh: ["Django", "M2M", "Transactions", "E-commerce"],
    kiungo: "../P12-biashara-django/",
    kiungo_maandishi: "Fungua folda ya mradi",
    maelezo_zaidi: "Endesha: cd P12-biashara-django; python manage.py runserver (admin/duka123, hassan/muuz123)",
  },
  {
    id: "P13",
    jina: "Mjibu (AI/RAG)",
    hali: "done",
    maelezo: "Uliza swali kwenye PDF/MD: FastAPI + Chroma (vector DB) + embeddings + LLM mbadala (Ollama/wingu) + citations + UI (tests 30).",
    tekh: ["FastAPI", "RAG", "Chroma", "Ollama"],
    kiungo: "../P13-mjibu-rag/",
    kiungo_maandishi: "Fungua folda ya mradi",
    maelezo_zaidi: "Endesha: cd P13-mjibu-rag; ollama serve; python -m uvicorn mjibu.app:app --port 8002",
  },
];

function onyeshaMiradi(kichujio) {
  const sanduku = document.getElementById("projects");
  sanduku.innerHTML = "";
  miradi
    .filter((m) => kichujio === "zote" || m.hali === kichujio)
    .forEach((m) => {
      const kadi = document.createElement("div");
      kadi.className = "card projekti";
      kadi.tabIndex = 0;
      const alama =
        m.hali === "done"
          ? '<span class="alama done">Imekamilika</span>'
          : '<span class="alama coming">Inakuja</span>';
      kadi.innerHTML =
        alama +
        "<h3>" +
        m.id +
        " - " +
        m.jina +
        "</h3><p>" +
        m.maelezo +
        '</p><p class="teknolojia">' +
        m.tekh.join(" | ") +
        '</p><p class="fungua-dokezo">Bonyeza kufungua &#8594;</p>';
      kadi.addEventListener("click", () => funguaMradi(m));
      kadi.addEventListener("keydown", (e) => {
        if (e.key === "Enter") funguaMradi(m);
      });
      sanduku.appendChild(kadi);
    });
}

function funguaMradi(m) {
  const dirisha = document.getElementById("dirisha");
  let kiungoHTML = "";
  if (m.hali === "done" && m.kiungo) {
    kiungoHTML =
      '<a class="btn" href="' +
      m.kiungo +
      '" target="_blank">' +
      m.kiungo_maandishi +
      "</a>";
  } else if (m.hali === "coming") {
    kiungoHTML = '<span class="alama coming">Bado haijajengwa - angalia ramani</span>';
  }
  document.getElementById("dirisha-maadhi").innerHTML =
    '<span class="alama ' +
    (m.hali === "done" ? "done" : "coming") +
    '">' +
    (m.hali === "done" ? "Imekamilika" : "Inakuja") +
    "</span><h3>" +
    m.id +
    " - " +
    m.jina +
    "</h3><p>" +
    m.maelezo +
    '</p><p class="teknolojia">' +
    m.tekh.join(" | ") +
    "</p><p><b>Jinsi ya kuendesha:</b> " +
    m.maelezo_zaidi +
    "</p><p>" +
    kiungoHTML +
    "</p>";
  dirisha.classList.add("imefunguliwa");
}

function fungaDirisha() {
  document.getElementById("dirisha").classList.remove("imefunguliwa");
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("fungua-funga").addEventListener("click", fungaDirisha);
  document.getElementById("dirisha").addEventListener("click", (e) => {
    if (e.target.id === "dirisha") fungaDirisha();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") fungaDirisha();
  });
});

const vitufe = document.querySelectorAll(".kichujio");
vitufe.forEach((btn) => {
  btn.addEventListener("click", () => {
    vitufe.forEach((b) => b.classList.remove("kilichochaguliwa"));
    btn.classList.add("kilichochaguliwa");
    onyeshaMiradi(btn.dataset.kichujio);
  });
});

document.getElementById("mwaka").textContent = new Date().getFullYear();

onyeshaMiradi("done");
