/*
 Напишите запрос, выводящий список предметов, на изучение которых отведено максимальное количество часов.
*/

WITH SubjHours AS (
    SELECT MAX("HOUR") AS maximum_hour
    FROM "SUBJECT"
)

SELECT
    "SUBJECT"."SUBJ_NAME" AS name_of_subject
FROM "SUBJECT"
WHERE "SUBJECT"."HOUR" = (SELECT maximum_hour FROM SubjHours);
