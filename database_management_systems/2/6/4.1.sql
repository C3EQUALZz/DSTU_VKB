CREATE TABLE "EXAM_MARKS_NEW1" 
("EXAM_ID" INTEGER,
"STUDENT_ID" INTEGER,
"SUBJ_ID" INTEGER,
"MARK" INTEGER,
"EXAM_DATE" DATE,
CONSTRAINT "EXAM_OGR" PRIMARY KEY("STUDENT_ID", "EXAM_ID", "SUBJ_ID"))