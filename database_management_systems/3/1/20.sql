/*
 Вывести количество владельцев автомобилей, заданного цвета. Цвет вводится с клавиатуры.
 */

SELECT
    "AUTO"."C_OWNER" AS owners,
    COUNT(*) AS count_of_auto
FROM "MENU" INNER JOIN "AUTO" ON "AUTO"."C_COLOR" = "MENU"."C_MENU" || "MENU"."C_REC"
WHERE "MENU"."NAME_REC" = 'зеленый'
GROUP BY "AUTO"."C_OWNER"