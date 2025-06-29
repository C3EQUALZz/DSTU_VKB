create user viewer WITH PASSWORD 'read_only_pass';
grant connect on database fourth_laboratory_database TO viewer;
grant usage on schema public TO viewer;
grant select on weather to viewer;
grant select on all tables in schema public TO viewer;

create user editor with password 'edit_pass';
grant connect on database fourth_laboratory_database TO editor;
grant usage on schema public TO editor;
grant select, update on weather to editor;
grant select, update on all tables in schema public TO editor;

grant select, update, insert on weather to postgres;