/*
 Для обучающихся студентов посчитать количество дисциплин (без повторов),
 которые будут им преподаваться в следующем семестре
 (текущий семестр установлен у объекта «Студент»).
 */

SELECT "Persons"."IDPersons",
COUNT(DISTINCT "Приказы"."Код Приказа"),
COUNT(CASE WHEN "Приказы"."Проведен"='true' THEN 1 END)
FROM "Persons" 
JOIN "PersonT" 
ON "Persons"."IDPersons"="PersonT"."IngPerson"
JOIN "StudentsT"
ON "PersonT"."IDPerson"="StudentsT"."IDPerson"
JOIN "ПриказыПоСтудентам" 
ON "StudentsT"."IDStudent"="ПриказыПоСтудентам"."КодСтудента"
JOIN "Приказы"
ON "ПриказыПоСтудентам"."КодПриказа"="Приказы"."Код Приказа"
WHERE "Приказы"."ДатаРегистрации" IS NOT NULL
GROUP BY "Persons"."IDPersons"