SELECT "UNIV_NAME", MAX("BIRTHDAY")
FROM "UNIVERSITY" JOIN "STUDENT"
ON "UNIVERSITY"."UNIV_ID" = "STUDENT"."UNIV_ID"
GROUP BY "UNIV_NAME"