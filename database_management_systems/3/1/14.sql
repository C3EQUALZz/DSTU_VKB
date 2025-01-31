/*
 Написать запрос, который выводит номер автомобиля и название его класса.
 Если класс не определен, то вывести сообщение «класс не определен» (использовать left join).
*/

SELECT "AUTO"."INV", COALESCE("MENU"."NAME_REC", 'класс не определён')
FROM "AUTO"
         LEFT JOIN "MENU" ON "AUTO"."C_CLASS" = ("MENU"."C_MENU" || "MENU"."C_REC")
