SELECT "EXAM_DATE", COUNT("STUDENT_ID") 
FROM "EXAM_MARKS" 
GROUP BY "EXAM_DATE";