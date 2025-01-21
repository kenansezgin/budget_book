SELECT name
FROM sqlite_master
WHERE type = 'table'
    AND name = 'monatsübersicht';
SELECT *
FROM monatsübersicht;