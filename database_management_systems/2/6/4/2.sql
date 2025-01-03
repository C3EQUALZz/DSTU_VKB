/*
 Создайте таблицу предметов обучения SUBJECT2 так, чтобы количество отводимых на предмет часов по
 умолчанию было равно 36, не допускались записи с отсутствующим количеством часов, поле SUBJ_ID
 являлось первичным ключом таблицы, а значения семестров (поле SEMESTR) лежали в диапазоне от 1 до 12.
 */

CREATE TABLE "SUBJECT2"
(
    "SUBJ_ID"   INTEGER PRIMARY KEY,
    "SUBJ_NAME" VARCHAR,
    "HOUR"      INTEGER NOT NULL DEFAULT '36',
    "SEMESTR"   INTEGER CHECK ("SEMESTR" IN (1, 12))
);

INSERT INTO "SUBJECT2" ("SUBJ_ID", "SUBJ_NAME", "SEMESTR")
VALUES ('1', 'PRO', '12')