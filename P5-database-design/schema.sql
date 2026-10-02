-- ============================================================
-- P5 - SCHEMA: Mfumo wa Mikopo na Usajili (database design)
-- Inafanya kazi na SQLite (Python) - maoni ya PostgreSQL yameonyeshwa
-- Endesha: python fanya.py
-- ============================================================

PRAGMA foreign_keys = ON;

-- HATUA 1: wateja (wateja wa mfumo - "mali" kuu)
CREATE TABLE IF NOT EXISTS wateja (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    jina        TEXT NOT NULL,
    simu        TEXT UNIQUE,
    barua_pepe  TEXT,
    tangu       DATE DEFAULT (DATE('now'))
);

-- HATUA 2: watumiaji wa mfumo (wafanyakazi - wanaofungua kwenye P6)
-- nenosiri HAKIPASWI kuwa wazi: hifadhi hash (3.1 uliojifunza!)
CREATE TABLE IF NOT EXISTS watumiaji (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    jina_la_mtumiaji TEXT NOT NULL UNIQUE,
    nenosiri_hash    TEXT NOT NULL,
    jukumu           TEXT NOT NULL CHECK (jukumu IN ('admin','mpokeaji','mhasibu')),
    tangu            DATE DEFAULT (DATE('now'))
);

-- HATUA 3: mikopo (kituo cha mfumo - kila mkopo umehusishwa na 2 watu)
CREATE TABLE IF NOT EXISTS mikopo (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    mteja_id        INTEGER NOT NULL,
    aliyeandika_id  INTEGER NOT NULL,
    kiasi           REAL NOT NULL CHECK (kiasi > 0),
    riba            REAL NOT NULL CHECK (riba >= 0 AND riba <= 100),
    miezi           INTEGER NOT NULL CHECK (miezi BETWEEN 1 AND 360),
    aina            TEXT NOT NULL CHECK (aina IN ('flat','reducing')),
    tangu           DATE DEFAULT (DATE('now')),
    FOREIGN KEY (mteja_id) REFERENCES wateja(id) ON DELETE RESTRICT,
    FOREIGN KEY (aliyeandika_id) REFERENCES watumiaji(id)
);

-- HATUA 4: malipo (kila mloka - ONDELETE CASCADE kwa sababu
-- malipo hayawezi kuishi bila mkopo wao)
CREATE TABLE IF NOT EXISTS malipo (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    mkopo_id INTEGER NOT NULL,
    kiasi    REAL NOT NULL CHECK (kiasi > 0),
    tarehe   DATE DEFAULT (DATE('now')),
    njia     TEXT CHECK (njia IN ('fedha','benki','m-pesa')),
    FOREIGN KEY (mkopo_id) REFERENCES mikopo(id) ON DELETE CASCADE
);

-- INDEX: kwa kasi ya maswali (kama "kamashifuti" la vitabu)
CREATE INDEX IF NOT EXISTS idx_mikopo_mteja ON mikopo(mteja_id);
CREATE INDEX IF NOT EXISTS idx_malipo_mkopo ON malipo(mkopo_id);

-- VIEW: "dirisha" linaloonyesha deni halisi bila kuandika SQL kila mara
CREATE VIEW IF NOT EXISTS deni_halisi AS
SELECT m.id AS mkopo_id,
       w.jina AS mteja,
       m.kiasi AS asilia,
       COALESCE(SUM(p.kiasi), 0) AS imeolishwa,
       m.kiasi - COALESCE(SUM(p.kiasi), 0) AS inayobaki,
       m.aina,
       m.miezi
FROM mikopo m
JOIN wateja w ON w.id = m.mteja_id
LEFT JOIN malipo p ON p.mkopo_id = m.id
GROUP BY m.id;

-- TRIGGER: kumbukumbu OTOMATIKI - database yenyewe inaandika
-- kila malipo yanapoingia (bila programu kuita kitu chochote!)
CREATE TABLE IF NOT EXISTS kumbukumbu_za_malipo (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    mkopo_id INTEGER NOT NULL,
    kiasi   REAL NOT NULL,
    wakati  TEXT DEFAULT (DATETIME('now')),
    FOREIGN KEY (mkopo_id) REFERENCES mikopo(id)
);

CREATE TRIGGER IF NOT EXISTS malipo_yaingie
AFTER INSERT ON malipo
BEGIN
    INSERT INTO kumbukumbu_za_malipo (mkopo_id, kiasi)
    VALUES (NEW.mkopo_id, NEW.kiasi);
END;
