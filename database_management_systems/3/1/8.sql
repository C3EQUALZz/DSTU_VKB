/*
 Определить количество автомобилей заданного владельца, номер гос. регистрации которых начинается на «00»
 и не заканчивается на «ду».
*/

SELECT
    COUNT(*) AS count_of_auto,
    "C_OWNER" AS owner
FROM "AUTO"
WHERE "SIGN" LIKE '00%ду'
GROUP BY "C_OWNER"