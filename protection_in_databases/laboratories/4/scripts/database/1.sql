create table if not exists temporary_object(
	id serial,
	time_create timestamp not null,
	time_dead timestamp,
	primary key(id, time_create)
);

create table if not exists city(
	id serial primary key,
	name varchar(90) not null
);

create table if not exists temperature(
	id integer not null,
	time_create timestamp,
	city_id integer,
	temperature integer check (temperature > -99 and temperature < 99),
	foreign key (city_id) references city(id) on delete cascade on update cascade
);

create table if not exists wind_direction(
	id integer not null,
	time_create timestamp,
	city_id integer,
	direction varchar(2) check (direction in ('С', 'Ю', 'В', 'З', 'СВ', 'СЗ', 'ЮВ', 'ЮЗ')),
	foreign key (city_id) references city(id) on delete cascade on update cascade
);

create table if not exists temperature_journal(
	city_id integer,
	temperature integer check (temperature > -99 and temperature < 99),
	primary key(id, time_create)
)inherits (temporary_object);

create table if not exists wind_direction_journal(
	city_id integer,
	direction varchar(2) check (direction in ('С', 'Ю', 'В', 'З', 'СВ', 'СЗ', 'ЮВ', 'ЮЗ')),
	primary key(id, time_create)
)inherits (temporary_object);