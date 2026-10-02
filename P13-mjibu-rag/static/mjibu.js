const mazungumzo = document.getElementById("mazungumzo");

function ongezaUjumbe(side, maandishi, vyanzo) {
  const d = document.createElement("div");
  d.className = "ujumbe " + (side === "mtumiaji" ? "mtumiaji-msg" : "uwezo");
  d.textContent = (side === "mtumiaji" ? "" : "Mjibu: ") + maandishi;
  if (vyanzo && vyanzo.length) {
    const c = document.createElement("div");
    c.className = "vyanzo-chips";
    vyanzo.forEach(v => {
      const s = document.createElement("span");
      s.className = "chip";
      s.textContent = "[?] " + v.jina + " #" + v.namba + " (" + v.alama + ")";
      s.textContent = s.textContent.replace("[?]", "[" + (vyanzo.indexOf(v) + 1) + "]");
      c.appendChild(s);
    });
    d.appendChild(c);
  }
  mazungumzo.appendChild(d);
  mazungumzo.scrollTop = mazungumzo.scrollHeight;
}

async function onyeshaNyaraka() {
  const r = await fetch("/api/nyaraka");
  const data = await r.json();
  const ul = document.getElementById("orodha");
  ul.innerHTML = "";
  data.forEach(n => {
    const li = document.createElement("li");
    const span = document.createElement("span");
    span.textContent = n.jina + " (" + n.vipande + " vipande)";
    const b = document.createElement("button");
    b.type = "button";
    b.className = "futa";
    b.textContent = "futa";
    b.onclick = async () => {
      await fetch("/api/nyaraka/" + encodeURIComponent(n.jina),
                  { method: "DELETE" });
      onyeshaNyaraka();
    };
    li.appendChild(span);
    li.appendChild(b);
    ul.appendChild(li);
  });
}

document.getElementById("fomu-pakia").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = document.getElementById("faili");
  if (!f.files.length) return;
  const fd = new FormData();
  fd.append("faili", f.files[0]);
  const h = document.getElementById("hali-pakia");
  h.textContent = "Inapakia...";
  try {
    const r = await fetch("/api/pakia", { method: "POST", body: fd });
    const data = await r.json();
    if (!r.ok) { h.textContent = "Hitilafu: " + (data.detail || r.status); return; }
    h.textContent = "Imepakiwa: " + data.jina + " → vipande " + data.vipande;
    f.value = "";
    onyeshaNyaraka();
  } catch (err) { h.textContent = "Hitilafu ya mtandao: " + err; }
});

document.getElementById("fomu-swali").addEventListener("submit", async (e) => {
  e.preventDefault();
  const i = document.getElementById("swali");
  const swali = i.value.trim();
  if (!swali) return;
  ongezaUjumbe("mtumiaji", swali);
  i.value = "";
  const btn = document.getElementById("tuma");
  btn.classList.add("inasakinisha");
  btn.textContent = "Inafikiri...";
  try {
    const r = await fetch("/api/swali", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ swali }),
    });
    const data = await r.json();
    ongezaUjumbe("mjawibu", data.jibu, data.vyanzo);
  } catch (err) {
    ongezaUjumbe("mjawibu", "Hitilafu ya mtandao: " + err);
  } finally {
    btn.classList.remove("inasakinisha");
    btn.textContent = "Tuma";
  }
});

onyeshaNyaraka();
