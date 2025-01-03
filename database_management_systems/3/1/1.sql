/*
 Напишите запрос, который выбирает все автомобили определенного цвета и находит средний год их выпуска.
 Цвет задается в виде параметра (например, «белый»). Нулевые не учитывать.
*/

-- SELECT *
-- FROM "AUTO"
-- WHERE "C_COLOR" =
--       (SELECT "C_MENU" || "C_REC"
--        FROM "MENU"
--        WHERE "NAME_REC" = 'белый')

SELECT "C_MENU" || "C_REC"
       FROM "MENU"
       WHERE "NAME_REC" = 'белый'