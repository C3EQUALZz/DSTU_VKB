/*
 По каждому человеку вывести количество всех зарегистрированных приказов
 (т.е. дата регистрации не пустая), а также количеств зарегистрированных приказов,
 которые были проведены.
 */

SELECT "Persons"."IDPersons",
       COUNT(DISTINCT "Приказы"."Код Приказа") AS registered_orders,
       COUNT(CASE WHEN "Приказы"."Проведен" = 'true' THEN 1 END) AS registered_orders_that_have_been_carried_out
FROM "Persons"
         JOIN "PersonT"
              ON "Persons"."IDPersons" = "PersonT"."IngPerson"
         JOIN "StudentsT"
              ON "PersonT"."IDPerson" = "StudentsT"."IDPerson"
         JOIN "ПриказыПоСтудентам"
              ON "StudentsT"."IDStudent" = "ПриказыПоСтудентам"."КодСтудента"
         JOIN "Приказы"
              ON "ПриказыПоСтудентам"."КодПриказа" = "Приказы"."Код Приказа"
WHERE "Приказы"."ДатаРегистрации" IS NOT NULL
GROUP BY "Persons"."IDPersons"