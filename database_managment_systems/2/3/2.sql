SELECT SUBSTR("NAME", 1,1)||'.'||UPPER("SURNAME")||';'||' место жительства'||' -- '||UPPER("CITY")||';'||' родился'||' -- '||
TO_CHAR("BIRTHDAY",'DD.MM.YY')
FROM "STUDENT"