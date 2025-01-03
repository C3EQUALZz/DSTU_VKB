/*
 Вывести автомобиль(и), у которых наибольший период от ввода в эксплуатацию до даты тех. паспорта среди автомобилей,
 номера которых заканчиваются на «рду».
*/

SELECT *
FROM "AUTO"
WHERE "SIGN" LIKE '%рду' AND "D_PASS" - "D_EXPL" = (
    SELECT MAX("D_PASS" - "D_EXPL")
    FROM "AUTO"
    WHERE "SIGN" LIKE '%рду'
);