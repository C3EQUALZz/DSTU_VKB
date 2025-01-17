/**
  Реализовать базовое отношение my_object, содержащее атрибуты:
    •	id – идентификатор записи, тип: integer;
    •	time_create – время создания записи (время рождения), тип timestamp;
    •	time_dead – время смерти записи, тип timestamp.
  Первичный ключ (Primary Key): {id, time_create}
*/

DROP TABLE IF EXISTS my_object CASCADE;

CREATE TABLE my_object
(
    id          INT,
    time_create TIMESTAMP,
    time_dead   TIMESTAMP,
    CONSTRAINT prim PRIMARY KEY (id, time_create)
);