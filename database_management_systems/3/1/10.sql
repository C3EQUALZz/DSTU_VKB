/*
Напишите запрос, который выводит название марки, средняя цена автомобиля для которой наибольшая. Нулевые не учитывать.
*/

SELECT "C_MARK"
FROM "AUTO"
GROUP BY "C_MARK"
ORDER BY AVG("COST") DESC
LIMIT 1