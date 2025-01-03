/*
 Напишите запрос, который выбирает все автомобили, произведенные на заданном заводе–изготовителя и находит количество
 номеров тех.паспорта начинающихся на символы «ШП».
 Завод-изготовителя задается в виде параметра (например, «АЗЛК, СССР»).
 */

CREATE OR REPLACE FUNCTION count_passports_by_plant(plant_param TEXT)
    RETURNS INTEGER
    LANGUAGE plpgsql AS
'
    BEGIN
        RETURN (SELECT COUNT("AUTO"."N_PASS")
                FROM "AUTO"
                         INNER JOIN "MENU" ON "AUTO"."C_PLANT" = ("MENU"."C_MENU" || "MENU"."C_REC")
                WHERE "MENU"."NAME_REC" = plant_param
                  AND "AUTO"."N_PASS" LIKE ''ШП%'');
    END;
';


SELECT count_passports_by_plant('АЗЛК, СССР');
