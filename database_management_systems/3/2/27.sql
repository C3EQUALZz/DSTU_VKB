/*
 Вывести первых 5 преподавателей, сумма аудиторных часов за текущий семестр у которых наибольшая.
 Список пронумеровать в порядке убывания количества аудиторных часов.
 */

SELECT "IDPrepod", "PrepodFamIO", SUM("Plany"."PAuditTime")
FROM "Prepod"
JOIN "Plany" 
ON "Prepod"."IDPrepod" = "Plany"."IDPlany"
WHERE "Plany"."PSemestr" = 4
GROUP BY "Prepod"."IDPrepod"
ORDER BY SUM("Plany"."PAuditTime") DESC
LIMIT 5