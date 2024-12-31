SELECT "IDPrepod", "PrepodFamIO", SUM("Plany"."PAuditTime")
FROM "Prepod"
JOIN "Plany" 
ON "Prepod"."IDPrepod" = "Plany"."IDPlany"
WHERE "Plany"."PSemestr" = 4
GROUP BY "Prepod"."IDPrepod"
ORDER BY SUM("Plany"."PAuditTime") DESC
LIMIT 5