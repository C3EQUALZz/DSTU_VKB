/*
 Напишите запрос, который выбирает все автомобили определенной марки (модели) и находит количество автомобилей,
 номер которых не заканчивается на буквы «дб».
 Нулевые не учитывать. Марка задается в виде параметра (например, «москвич М-412»).
*/

CREATE OR REPLACE FUNCTION count_autos_by_brand(brand_param TEXT)
RETURNS INTEGER
LANGUAGE plpgsql AS '
    BEGIN
        RETURN (SELECT COUNT(*) AS count_of_auto
                FROM "AUTO"
                         JOIN "MENU" ON "AUTO"."C_MARK" = ("MENU"."C_MENU" || "MENU"."C_REC")
                WHERE "MENU"."NAME_REC" = brand_param
                  AND "AUTO"."SIGN" NOT LIKE ''%дб''
                  AND "AUTO"."SIGN" IS NOT NULL);
    END;
';

-- Вызов функции
SELECT count_autos_by_brand('москвич М-412');

