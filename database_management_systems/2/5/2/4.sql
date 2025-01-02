/*
 Напишите запрос для получения списка университетов вместе с названиями преподаваемых в них предметов.
 */

SELECT "UNIV_NAME", "SUBJ_NAME"
FROM "UNIVERSITY"
         JOIN "LECTURER"
              ON "UNIVERSITY"."UNIV_ID" = "LECTURER"."UNIV_ID"
         JOIN "SUBJ_LECT"
              ON "LECTURER"."LECTURER_ID" = "SUBJ_LECT"."LECTURER_ID"
         JOIN "SUBJECT"
              ON "SUBJ_LECT"."SUBJ_ID" = "SUBJECT"."SUBJ_ID"
GROUP BY "UNIV_NAME", "SUBJ_NAME"