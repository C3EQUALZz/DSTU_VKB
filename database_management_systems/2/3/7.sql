/*
 Составьте запрос для таблицы UNIVERSITY таким образом, чтобы выходная таблица содержала всего один
 столбец в следующем виде: Код-10; ВГУ-r. ВОРОНЕЖ; Рейтинг=296.
*/

SELECT
    CONCAT_WS('; ',
        'Код-' || "UNIV_ID",
        "UNIV_NAME" || '-г. ' || UPPER("CITY"),
        'Рейтинг=' || "RATING"
    ) AS university_info
FROM "UNIVERSITY";