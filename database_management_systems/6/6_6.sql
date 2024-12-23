create or replace function concat_strings(delim text, str1 text, str2 text)
returns text
language 'plpgsql'
as $BODY$
declare concat_res text;
begin
concat_res = str1 || delim || str2;
return concat_res;
end $BODY$
