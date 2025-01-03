/*
 Напишите запрос, который выбирает все автомобили определенного цвета и находит средний год их выпуска.
 Цвет задается в виде параметра (например, «белый»). Нулевые не учитывать.
*/

CREATE OR REPLACE FUNCTION get_average_year_by_color(color_param TEXT)
    RETURNS NUMERIC
    LANGUAGE plpgsql
    AS
'
    BEGIN
        RETURN (SELECT AVG("AUTO"."YEAR_A") AS average_year
                FROM "AUTO"
                         JOIN "MENU" ON "AUTO"."C_COLOR" = ("MENU"."C_MENU" || "MENU"."C_REC")
                WHERE "MENU"."NAME_REC" = color_param
                  AND "AUTO"."YEAR_A" IS NOT NULL);
    END;
';

SELECT get_average_year_by_color('белый');
