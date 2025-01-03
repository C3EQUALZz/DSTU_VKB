/*
 Напишите запрос, который выводит все автомобили определенной марки с заданным типом кузова.
 Марка и кузов задаются как параметр (например, «М-67-36 б/коляски» и «седан»).
*/

CREATE OR REPLACE FUNCTION get_id_from_menu_by_text(brand_param TEXT)
    RETURNS TEXT
    LANGUAGE plpgsql AS
'
    BEGIN
        RETURN (SELECT "C_MENU" || "C_REC"
                FROM "MENU"
                WHERE "NAME_REC" = brand_param);
    END;
';

SELECT *
FROM "AUTO"
WHERE "C_MARK" = get_id_from_menu_by_text('ВАЗ-21061')
   OR "C_BODY" = get_id_from_menu_by_text('хечбек')
