--ЗАДАНИЕ 1

DROP TABLE IF EXISTS my_object CASCADE;
CREATE TABLE my_object (
	id INT,
	time_create TIMESTAMP,
	time_dead TIMESTAMP,
	CONSTRAINT prim
		PRIMARY KEY(id, time_create)
);

--ЗАДАНИЕ 2
DROP TABLE IF EXISTS object1 CASCADE;
CREATE TABLE object1 (
    description VARCHAR(100)
) INHERITS (my_object);

DROP TABLE IF EXISTS object2 CASCADE;
CREATE TABLE object2 (
    selfworth INT
) INHERITS (my_object);

DROP TABLE IF EXISTS object3 CASCADE; 
CREATE TABLE object3 (
    in_group INT
) INHERITS (my_object);

--ЗАДАНИЕ 3

CREATE OR REPLACE FUNCTION insert_log() RETURNS TRIGGER AS $emp_audit$
    BEGIN
		IF EXISTS(SELECT * FROM my_object
				  WHERE my_object.id = NEW.id and time_dead IS NOT NULL) THEN
		  UPDATE my_object
		  SET time_dead = CURRENT_TIMESTAMP
		  WHERE (my_object.id = NEW.id) AND (time_dead IS NOT NULL);
		  INSERT INTO my_object (id, time_create)
		  VALUES (NEW.id, CURRENT_TIMESTAMP);
		  ELSE
		  INSERT INTO my_object (id, time_create)
		  VALUES (NEW.id, CURRENT_TIMESTAMP);
		END IF;
        RETURN NULL;
    END;
$emp_audit$ LANGUAGE plpgsql;

CREATE TRIGGER emp_audit BEFORE INSERT ON my_object
    FOR EACH ROW EXECUTE FUNCTION insert_log();

INSERT INTO my_object(id)
VALUES (1)