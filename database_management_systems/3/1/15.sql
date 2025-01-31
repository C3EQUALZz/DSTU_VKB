/*
 Определить, сколько автомобилей каждой марки имеют год выпуска меньший, чем округленный до целого средний год
 выпуска автомобилей заданной пользователем марки (использовать подзапрос).
 Задать название марки (например, «М-67-36 б/коляски»).
 */

SELECT
    "AUTO"."C_MARK", COUNT("AUTO"."C_MARK")
FROM "AUTO"
WHERE "AUTO"."YEA_" < (SELECT ROUND(AVG("AUTO"."YEA_"))
                       FROM "AUTO"
                                LEFT JOIN "MENU" ON "AUTO"."C_CLASS" = ("MENU"."C_MENU" || "MENU"."C_REC")
                       WHERE "MENU"."NAME_REC" = 'особо малый класс')
GROUP BY "AUTO"."C_MARK"