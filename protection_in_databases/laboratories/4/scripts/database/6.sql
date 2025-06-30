CREATE OR REPLACE FUNCTION update_weather()
RETURNS TRIGGER AS $$
DECLARE
    city_id_var INT;
BEGIN
    SELECT id INTO city_id_var FROM city WHERE name = NEW.name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Город % не найден', NEW.name;
    END IF;

    UPDATE temperature
    SET time_create = NEW.temp_time,
        temperature = NEW.temperature
    WHERE city_id = city_id_var;

    UPDATE wind_direction
    SET time_create = NEW.wind_time,
        direction = NEW.direction
    WHERE city_id = city_id_var;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_weather
INSTEAD OF UPDATE ON weather
FOR EACH ROW EXECUTE FUNCTION update_weather();