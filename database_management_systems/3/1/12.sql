/*
 По каждой штатной группе автомобилей определить сколько а/м каждой марки было выпущено в заданном году.
 Вывести названия групп и названия марок на экран. Год задается параметром (например, 1989).
*/

SELECT
    "C_GROUP" AS code_of_group,
    "C_MARK" AS code_of_mark,
    COUNT("C_MARK") AS count_of_marks
FROM "AUTO"
WHERE "YEAR_A" = 1991
GROUP BY "C_GROUP", "C_MARK";
