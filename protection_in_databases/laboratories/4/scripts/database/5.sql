create view weather as
select c.name, t.time_create as temp_time, t.temperature, w.time_create as wind_time, w.direction as direction
from city as c
inner join temperature as t on t.city_id = c.id
inner join wind_direction as w on w.city_id = c.id
order by c.id;