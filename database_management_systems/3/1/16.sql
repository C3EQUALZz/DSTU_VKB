/*
 Определить какое количество автомобилей каждой марки в каком году было произведено
 (использовать перекрестный запрос). Нулевые марки не учитывать.
 */

SELECT
    a1."C_MARK" AS mark,
    COUNT(a1."C_MARK") AS count_of_auto,
    a2."YEA_" AS year
FROM "AUTO" AS a1 CROSS JOIN "AUTO" AS a2
GROUP BY a1."C_MARK", a2."YEA_"