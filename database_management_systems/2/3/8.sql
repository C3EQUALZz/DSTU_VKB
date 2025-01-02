/*
 То же; что и в упр. 7, но значения рейтинга требуется округлить до
 первого знака (например, значение -382 округляется-до 400).
*/

SELECT
    CONCAT_WS('; ',
        'Код-' || "UNIV_ID",
        "UNIV_NAME" || '-г. ' || UPPER("CITY"),
        'Рейтинг=' || ROUND("RATING", -2)
    ) AS university_info
FROM "UNIVERSITY"
