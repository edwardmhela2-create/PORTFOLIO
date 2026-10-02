-- MASWALI (queries) ya kujifunza - kila moja inaonyeshwa na fanya.py

-- 1. Mikopo yote na majina ya wateja na waliyeandika (JOIN ya vitatu)
SELECT m.id, w.jina AS mteja, u.jina_la_mtumiaji AS mpokeaji,
       m.kiasi, m.riba, m.miezi, m.aina
FROM mikopo m
JOIN wateja w ON w.id = m.mteja_id
JOIN watumiaji u ON u.id = m.aliyeandika_id
ORDER BY m.id;

-- 2. Kila mkopo: kiasi kilicholipwa na kilichobaki (LEFT JOIN + GROUP BY)
SELECT m.id, w.jina, m.kiasi,
       COALESCE(SUM(p.kiasi), 0) AS imeolishwa,
       m.kiasi - COALESCE(SUM(p.kiasi), 0) AS inayobaki
FROM mikopo m
JOIN wateja w ON w.id = m.mteja_id
LEFT JOIN malipo p ON p.mkopo_id = m.id
GROUP BY m.id;

-- 3. Jumla ya deni kwa kila mteja (GROUP BY)
SELECT w.jina, COUNT(m.id) AS mikopo, SUM(m.kiasi) AS jumla
FROM wateja w
JOIN mikopo m ON m.mteja_id = w.id
GROUP BY w.id
ORDER BY jumla DESC;

-- 4. Nani anadai zaidi? (subquery ndogo: anayeongoza pekee)
SELECT w.jina, SUM(m.kiasi) AS jumla
FROM wateja w
JOIN mikopo m ON m.mteja_id = w.id
GROUP BY w.id
ORDER BY jumla DESC
LIMIT 1;

-- 5. View: deni halisi (baada ya malipo)
SELECT * FROM deni_halisi;

-- 6. Malipo kwa njia (m-pesa, benki, fedha - GROUP BY)
SELECT njia, COUNT(id) AS idadi, SUM(kiasi) AS jumla
FROM malipo
GROUP BY njia
ORDER BY jumla DESC;

-- 7. Wateja wasio na mikopo (LEFT JOIN + IS NULL)
SELECT w.jina
FROM wateja w
LEFT JOIN mikopo m ON m.mteja_id = w.id
WHERE m.id IS NULL;

-- 8. Wastani wa mkopo kwa aina (AVG + GROUP BY)
SELECT aina, COUNT(id) AS idadi, ROUND(AVG(kiasi), 0) AS wastani
FROM mikopo
GROUP BY aina;

-- 9. HAVING: jumla kwa mteja NA uchujaji wa kundi (GROUP BY + HAVING)
SELECT w.jina, COUNT(m.id) AS mikopo, SUM(m.kiasi) AS jumla
FROM wateja w
JOIN mikopo m ON m.mteja_id = w.id
GROUP BY w.id
HAVING SUM(m.kiasi) > 500000
ORDER BY jumla DESC;

-- 10. Subquery: malipo makubwa kuliko wastani wa malipo yote
SELECT p.id, p.mkopo_id, p.kiasi, p.njia
FROM malipo p
WHERE p.kiasi > (SELECT AVG(kiasi) FROM malipo)
ORDER BY p.kiasi DESC;
