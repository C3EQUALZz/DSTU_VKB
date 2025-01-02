/*
 Напишите запрос SELECT, который для каждого предмета обучения (SUBJECT)
 выполняет вывод его наименования (SUBJ_NAMЕ) и следом за ним количества часов (HOUR) в 4-м семестре (SEMESTR).
*/

SELECT
    "SUBJ_NAME",
    "HOUR"
FROM "SUBJECT"
WHERE "SEMESTR" = 4