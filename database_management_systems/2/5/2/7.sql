/*
 Напишите запрос для получения списка преподавателей с указанием суммарного количества часов,
 отведенных для обучения каждому из предметов.
 */

SELECT "SURNAME", "HOUR", "SUBJ_NAME"
FROM "LECTURER"
         JOIN "SUBJ_LECT"
              ON "LECTURER"."LECTURER_ID" = "SUBJ_LECT"."LECTURER_ID"
         JOIN "SUBJECT"
              ON "SUBJ_LECT"."SUBJ_ID" = "SUBJECT"."SUBJ_ID"
GROUP BY "SURNAME", "HOUR", "SUBJ_NAME"