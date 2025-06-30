create index city_index on city(id);
create index temporary_object_index on temporary_object(id, time_create);
create index temperature_index on temperature(id, city_id);
create index wind_direction_index on wind_direction(id, city_id);
create index temperature_journal_index on temperature_journal(id, time_create);
create index wind_direction_journal_index on wind_direction_journal(id, time_create);
