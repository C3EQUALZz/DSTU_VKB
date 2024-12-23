SELECT "NAME"||' '||"SURNAME"||' '|| 'родился в' ||' '|| TO_CHAR("BIRTHDAY",'YYYY') ||' '||'году'
FROM "STUDENT"