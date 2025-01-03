/*
 Напишите команду, удаляющую из таблицы SUBJECT1 сведения о предметах обучения,
 по которым студентами не получено ни одной оценки.
*/

DROP TABLE IF EXISTS SUBJECT1;

CREATE TABLE SUBJECT1 AS (SELECT *
                          FROM "SUBJECT");

DELETE
FROM SUBJECT1
WHERE "SUBJ_ID" NOT IN (SELECT DISTINCT("SUBJECT"."SUBJ_ID")
                        FROM "EXAM_MARKS"
                                 INNER JOIN "SUBJECT"
                                            ON "SUBJECT"."SUBJ_ID" = "EXAM_MARKS"."SUBJ_ID" AND "MARK" IS NOT NULL);