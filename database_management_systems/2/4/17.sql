/*
 Для каждого университета напишите запрос, выводящий сумму стипендии, выплачиваемой студентам каждого курса.
 */

SELECT SUM("STIPEND"),
       "UNIV_ID",
       "KURS"
FROM "STUDENT"
GROUP BY "UNIV_ID", "KURS"
ORDER BY "UNIV_ID", "KURS"