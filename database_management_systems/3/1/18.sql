/*
 Вывести сумму, которую потратил каждый владелец на автомобили. Нулевые цены не учитывать.
 */

SELECT
    "AUTO"."C_OWNER" AS owner,
    SUM("AUTO"."COST") AS summary_on_auto
FROM "AUTO"
WHERE "AUTO"."COST" IS NOT NULL AND "AUTO"."C_OWNER" IS NOT NULL
GROUP BY "AUTO"."C_OWNER"