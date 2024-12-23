SELECT LOWER(SUBSTR("NAME", 1,1))||'.'||LOWER("SURNAME")||';'||' место жительства'||' -- '||LOWER("CITY")||';'||' родился'||': '||
TO_CHAR("BIRTHDAY",'DD.Mon.YYYY')
FROM "STUDENT"