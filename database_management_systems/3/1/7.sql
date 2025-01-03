/*
 Напишите запрос, который считает среднюю стоимость для каждого из класса автомобилей.
*/

SELECT
    "C_CLASS" AS class_of_auto,
    ROUND(AVG("COST")::numeric, 2) AS cost
FROM "AUTO"
WHERE "C_CLASS" IS NOT NULL
GROUP BY "C_CLASS"