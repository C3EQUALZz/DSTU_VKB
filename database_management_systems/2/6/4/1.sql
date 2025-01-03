/*
 Создайте таблицу EXAM_MARKS так, чтобы не допускался ввод в таблицу двух записей об оценках одного
 студента по конкретным экзамену и предмету обучения.
 */

CREATE TABLE "EXAM_MARKS_NEW1"
(
    "EXAM_ID"    INTEGER,
    "STUDENT_ID" INTEGER,
    "SUBJ_ID"    INTEGER,
    "MARK"       INTEGER,
    "EXAM_DATE"  DATE,
    CONSTRAINT "EXAM_OGR" PRIMARY KEY ("STUDENT_ID", "EXAM_ID", "SUBJ_ID")
);

INSERT INTO "EXAM_MARKS_NEW1" ("EXAM_ID", "STUDENT_ID", "SUBJ_ID", "MARK", "EXAM_DATE")
VALUES ('100', '100', '100', '5', '2024-10-02')