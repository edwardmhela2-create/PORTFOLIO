PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS wateja (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    jina        TEXT NOT NULL,
    simu        TEXT UNIQUE,
    barua_pepe  TEXT,
    tangu       DATE DEFAULT (DATE('now'))
);

CREATE TABLE IF NOT EXISTS watumiaji (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    jina_la_mtumiaji TEXT NOT NULL UNIQUE,
    nenosiri_hash    TEXT NOT NULL,
    jukumu           TEXT NOT NULL CHECK (jukumu IN ('admin','mpokeaji','mhasibu')),
    tangu            DATE DEFAULT (DATE('now'))
);

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

CREATE TABLE IF NOT EXISTS malipo (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    mkopo_id INTEGER NOT NULL,
    kiasi    REAL NOT NULL CHECK (kiasi > 0),
    tarehe   DATE DEFAULT (DATE('now')),
    njia     TEXT CHECK (njia IN ('fedha','benki','m-pesa')),
    FOREIGN KEY (mkopo_id) REFERENCES mikopo(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_mikopo_mteja ON mikopo(mteja_id);
CREATE INDEX IF NOT EXISTS idx_malipo_mkopo ON malipo(mkopo_id);

CREATE TABLE IF NOT EXISTS kumbukumbu_za_malipo (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    mkopo_id INTEGER,
    kiasi   REAL NOT NULL,
    wakati  TEXT DEFAULT (DATETIME('now')),
    FOREIGN KEY (mkopo_id) REFERENCES mikopo(id) ON DELETE SET NULL
);

CREATE TRIGGER IF NOT EXISTS malipo_yaingie
AFTER INSERT ON malipo
BEGIN
    INSERT INTO kumbukumbu_za_malipo (mkopo_id, kiasi)
    VALUES (NEW.mkopo_id, NEW.kiasi);
END;
