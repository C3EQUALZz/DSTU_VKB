SELECT COUNT("LECTURER_ID"), "UNIV_ID"
FROM "LECTURER"
GROUP BY "UNIV_ID"
ORDER BY COUNT("LECTURER_ID") DESC