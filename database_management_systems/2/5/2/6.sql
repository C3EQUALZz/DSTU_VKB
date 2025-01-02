/*
 Напишите запрос для получения списка университетов с указанием суммарного количества часов,
 отводимых на изучение каждого предмета.
 */

SELECT "UNIV_NAME", "HOUR", "SUBJ_NAME"
FROM "UNIVERSITY"
         JOIN "LECTURER"
              ON "UNIVERSITY"."UNIV_ID" = "LECTURER"."UNIV_ID"
         JOIN "SUBJ_LECT"
              ON "LECTURER"."LECTURER_ID" = "SUBJ_LECT"."LECTURER_ID"
         JOIN "SUBJECT"
              ON "SUBJ_LECT"."SUBJ_ID" = "SUBJECT"."SUBJ_ID"
GROUP BY "UNIV_NAME", "HOUR", "SUBJ_NAME"