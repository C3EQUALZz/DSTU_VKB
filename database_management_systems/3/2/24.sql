/*
 Для всех записей о странах в таблице Addresses вывести количество человек (если нет, то 0),
 которые имеют эту страну в качестве своего адреса.
 Поиск проводить для всех мальчиков 4го курса и для девушек 9го семестра (только обучающиеся студенты).
 */

SELECT
    "Addresses"."AddrCountry" AS country,
    COUNT("Persons"."IDPersons") AS count_of_students
FROM "Persons"
    INNER JOIN "Addresses" ON "Persons"."IDPersons" = "Addresses"."IDВладельца"
    INNER JOIN "StudentsT" ON "Persons"."IDPersons" = "StudentsT"."IDPerson"
WHERE
    (("Persons"."Пол" = 'м' AND "StudentsT"."Semestr" IN (7, 8))
    OR
    ("Persons"."Пол" = 'ж' AND "StudentsT"."Semestr" = 9))
GROUP BY "Addresses"."AddrCountry"

