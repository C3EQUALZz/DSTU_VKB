insert into city (id, name) values
(1, 'Ростов-на-Дону'),
(2, 'Краснодар'),
(3, 'Москва');

insert into temperature (id, time_create, city_id, temperature) values
(1, current_timestamp, 1, 1),
(2, current_timestamp, 2, 5),
(3, current_timestamp, 3, -4);

insert into wind_direction (id, time_create, city_id, direction) values
(1, current_timestamp, 1, 'В'),
(2, current_timestamp, 2, 'В'),
(3, current_timestamp, 3, 'ЮВ');