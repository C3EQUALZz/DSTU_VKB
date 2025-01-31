/*
 Определить какое количество автомобилей каждого цвета к какой штатной группе относится
 (использовать перекрестный запрос). Нулевые штатные группы и цвета не учитывать.
*/

SELECT
    a1."C_GROUP" AS group_of_auto,
    "MENU"."NAME_REC" AS name_of_color,
    COUNT("MENU"."NAME_REC") AS count_of_auto
FROM "AUTO" AS a1 CROSS JOIN "AUTO" AS a2 INNER JOIN "MENU" ON a2."C_COLOR" = ("MENU"."C_MENU" || "MENU"."C_REC")
WHERE a1."C_GROUP" IS NOT NULL
GROUP BY a1."C_GROUP", "MENU"."NAME_REC"
