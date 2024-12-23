SELECT *
FROM "STUDENT"
WHERE (extract(year from current_date) - extract (year from("BIRTHDAY"))) > 30