/**
 То же, что и в упр. 4, но только для студентов 1, 2 и 4 курсов и таким образом, чтобы фамилии и имена были выведены прописными буквами.
*/

SELECT
    CONCAT_WS(' ', UPPER(CONCAT_WS(' ', "NAME", "SURNAME")), 'родился в', TO_CHAR("BIRTHDAY", 'YYYY'), 'году')
FROM "STUDENT"
WHERE "KURS" IN (1, 2, 4);