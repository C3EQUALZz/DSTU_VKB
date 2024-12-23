create function before_insert()
returns trigger
language 'plpgsql'
as $BODY$
begin
if (new.id in (select id from my_object)) then
update my_object
set time_dead = current_timestamp
where id = new.id;
end if;
return new;
end $BODY$;

create trigger before_insert_trigger
before insert on my_object
for each row execute function before_insert();

