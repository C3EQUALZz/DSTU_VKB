/*
 Напишите запрос, выводящий список университетов, расположенных в Москве и имеющих рейтинг меньший, чем у ВГУ.
 */

CREATE OR REPLACE FUNCTION get_university_rating(univ_name TEXT)
    RETURNS NUMERIC
    LANGUAGE plpgsql
    AS
'
    DECLARE
        university_rating NUMERIC; -- Переменная для хранения рейтинга
    BEGIN
        SELECT "RATING"
        INTO university_rating
        FROM "UNIVERSITY"
        WHERE LOWER("UNIV_NAME") = LOWER(univ_name);

        RETURN university_rating; -- Возвращаем рейтинг университета
    END;
';

SELECT "UNIVERSITY"."UNIV_NAME"
FROM "UNIVERSITY"
WHERE LOWER("UNIVERSITY"."CITY") = 'москва'
  AND "UNIVERSITY"."RATING" < get_university_rating('ВГУ')