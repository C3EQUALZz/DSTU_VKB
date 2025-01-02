/*
 Напишите запрос к таблице STUDENT для вывода списка всех студентов со стипендией не меньше 100,
 живущих в Воронеже, с указанием фамилии (SURNAME), имени (NAME) и номера курса (KURS)
 */

SELECT "SURNAME", "NAME", "KURS"
FROM "STUDENT"
WHERE "STIPEND" >= 100 AND "CITY" = 'Воронеж'