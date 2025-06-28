create function update_weather()
returns trigger as
$BODY$
begin
	update weather set
		temp_time = new.temp_time,
		temperature = new.temperature
		where name = new.name;
	return new;
end;
$BODY$
language 'plpgsql';

create trigger update_weather
instead of update on weather
for each row
execute function update_weather();