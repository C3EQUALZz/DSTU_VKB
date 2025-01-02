/*
 Для каждого предмета напишите запрос, выводящий количество преподавателей, ведущих по нему занятия
 */

WITH SubjectIDAndCountOfLectors AS (SELECT COUNT("LECTURER_ID") AS count_of_lectures,
                                           "SUBJ_ID"            AS subject_id
                                    FROM "SUBJ_LECT"
                                    GROUP BY "SUBJ_ID")

SELECT "SUBJECT"."SUBJ_NAME",
       SubjectIDAndCountOfLectors.count_of_lectures
FROM SubjectIDAndCountOfLectors
         INNER JOIN "SUBJECT" ON SubjectIDAndCountOfLectors.subject_id = "SUBJECT"."SUBJ_ID";