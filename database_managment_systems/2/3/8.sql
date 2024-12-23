SELECT 'Код'||'-'||"UNIV_ID"||'; '||"UNIV_NAME"||'-г. '||UPPER("CITY")||'; '||'Рейтинг'||'='||ROUND("RATING",-2)
FROM "UNIVERSITY"