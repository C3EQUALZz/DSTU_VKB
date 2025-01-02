SELECT *
FROM "AUTO"
WHERE "C_COLOR" =
      (SELECT "C_MENU" || "C_REC"
       FROM "MENU"
       WHERE "NAME_REC" = 'белый')
