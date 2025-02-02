/**
  Вывести все автомобили, в номерах которых есть сочетание "3р", а номер тех. паспорта начинается
  на "BMV".
 */

SELECT "INV","N_PASS", "SIGN"
FROM "AUTO" 
WHERE "N_PASS" LIKE 'BMV%' AND "SIGN" LIKE '%3р%'
