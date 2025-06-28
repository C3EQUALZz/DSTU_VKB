create or replace function check_previos_wind()
returns trigger as
$BODY$
declare
	current_t timestamp;
begin
	current_t = new.time_create;
	if new.id in (select id from wind_direction) then
		update wind_direction_journal set time_dead = current_t where wind_direction_journal.id = new.id;
		insert into wind_direction_journal(id, time_create, time_dead, city_id, direction) values
		(new.id, new.time_create, null, new.city_id, new.direction);
		update wind_direction set time_create = new.time_create where wind_direction.id = new.id;
		return null;
	else
		insert into wind_direction_journal(id, time_create, time_dead, city_id, direction) values
		(new.id, new.time_create, null, new.city_id, new.direction);
		return new;
	end if;
end;
$BODY$
language 'plpgsql';