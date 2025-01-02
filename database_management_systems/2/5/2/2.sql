/*
 Напишите запрос для получения списка преподавателей с указанием их учебных предметов.
 */

SELECT "SURNAME", "SUBJECT"."SUBJ_ID", "SUBJ_NAME"
FROM "LECTURER"
         JOIN "SUBJ_LECT"
              ON "LECTURER"."LECTURER_ID" = "SUBJ_LECT"."LECTURER_ID"
         JOIN "SUBJECT"
              ON "SUBJECT"."SUBJ_ID" = "SUBJ_LECT"."SUBJ_ID"
GROUP BY "SURNAME", "SUBJECT"."SUBJ_ID", "SUBJ_NAME"