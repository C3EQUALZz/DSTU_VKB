/*
 Для каждого преподавателя напишите запрос, выводящий количество преподаваемых им предметов.
*/

WITH CountOfSubjectsForEachLector AS (SELECT COUNT("SUBJ_ID") as count_of_subjects,
                                             "LECTURER_ID"    AS lecture_id
                                      FROM "SUBJ_LECT"
                                      GROUP BY "SUBJ_ID", "LECTURER_ID")

SELECT "LECTURER"."NAME",
       "LECTURER"."SURNAME",
       CountOfSubjectsForEachLector.count_of_subjects
FROM CountOfSubjectsForEachLector
         INNER JOIN "LECTURER" ON "LECTURER"."LECTURER_ID" = CountOfSubjectsForEachLector.lecture_id
