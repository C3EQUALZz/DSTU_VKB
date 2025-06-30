create or replace function check_previos_temp()
returns trigger as
$BODY$
declare 
	current_t timestamp;
begin
	current_t = new.time_create;
	if new.id in (select id from temperature) then
		update temperature_journal set time_dead = current_t where temperature_journal.id = new.id;
		insert into temperature_journal(id, time_create, time_dead, city_id, temperature) values
		(new.id, new.time_create, null, new.city_id, new.temperature);
		update temperature set time_create = new.time_create where temperature.id = new.id;
		return null;
	else
		insert into temperature_journal(id, time_create, time_dead, city_id, temperature) values
		(new.id, new.time_create, null, new.city_id, new.temperature);
		return new;
	end if;
end;
$BODY$
language 'plpgsql';

CREATE TRIGGER temp_journal_temporal
BEFORE INSERT ON temperature
FOR EACH ROW EXECUTE FUNCTION check_previos_temp();
