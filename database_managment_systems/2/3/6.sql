SELECT UPPER("NAME"||' '||"SURNAME")||' '|| 'родился в' ||' '|| TO_CHAR("BIRTHDAY",'YYYY') ||' '||'году'
FROM "STUDENT"
WHERE "KURS" IN (1,2,4)