UPDATE "STUDENT"
SET "STIPEND" = ("STIPEND" + (0.2 * "STIPEND"))
WHERE 6 <=
(SELECT SUM("MARK")
FROM "EXAM_MARKS"
WHERE "EXAM_MARKS"."STUDENT_ID" = "STUDENT"."STUDENT_ID")