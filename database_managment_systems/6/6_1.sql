create table my_object (
    id serial,
    time_create timestamp not null,
    time_dead timestamp,
    primary key (id, time_create)
) with (
    OIDS = false
);
