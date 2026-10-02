-- Data ya mfano (sample data) kwa kujaribu

INSERT INTO wateja (jina, simu, barua_pepe) VALUES
    ('Asha Hassan',  '0712345678', 'asha@example.com'),
    ('Juma Mhela',   '0755123456', 'juma@example.com'),
    ('Neema Shirima','0767123456', 'neema@example.com');

INSERT INTO watumiaji (jina_la_mtumiaji, nenosiri_hash, jukumu) VALUES
    ('admin',      'sha256$mfano$haujulikani', 'admin'),
    ('mpokeaji1',  'sha256$mfano2$haujulikani','mpokeaji');

INSERT INTO mikopo (mteja_id, aliyeandika_id, kiasi, riba, miezi, aina) VALUES
    (1, 2, 1000000, 15, 12, 'reducing'),
    (2, 2,  500000, 24,  6, 'flat'),
    (3, 1,  200000, 18,  4, 'reducing'),
    (1, 2,  300000, 20,  6, 'flat');

INSERT INTO malipo (mkopo_id, kiasi, njia) VALUES
    (1,  90258, 'benki'),
    (1,  90258, 'm-pesa'),
    (2,  93333, 'fedha'),
    (2,  93333, 'fedha'),
    (2,  93333, 'fedha'),
    (3,  54500, 'm-pesa');
