create function temporal_support.table_after_trigger()
returns trigger
security definer
language plpgsql as
$$
declare
    _history_schema constant text = '__history';
begin
    -- insert the old records into the history table
    execute format(
        $sql$
        insert into %1$I.%2$I select $1.*;
        $sql$,
        TG_TABLE_SCHEMA::text || _history_schema, TG_TABLE_NAME::text
    ) using old;
    -- after trigger ignores result
    return null;
end;
$$;



create function temporal_support.init_temporal_tables(
    variadic _tables text[]
)

returns void
security definer
language plpgsql as
$$
declare
    _record record;
    _command text;
    _history_schema text;
    _trigger_name constant text = 'temporal_support.table_after_trigger';
    _history_schema constant text = '__history';
begin
    for _record in (
        select table_schema, table_name
        from
            information_schema.tables tbl
            left join information_schema.triggers tr
            on tbl.table_schema = tr.event_object_schema
                and tbl.table_name = tr.event_object_table
                and tr.trigger_name = split_part(_trigger_name, '.', 2)
        where
            -- filter out tables that already have trigger
            tr.event_object_table is null
            -- schema.table in array or just table in array for public
            and (
                (table_schema <> 'public' and table_schema || '.' || table_name = any(_tables))
                or
                (table_schema = 'public' and table_name = any(_tables))
            )
            and table_type = 'BASE TABLE'
    )
    loop
        _history_schema = _record.table_schema || _history_schema;
        if not exists(
            select 1 from information_schema.tables
            where table_schema = _history_schema and table_name = _record.table_name
        ) then
            -- history table doesn't exists, create one based on actual table and add data valid field
            _command = format(
                $sql$
                create schema if not exists %1$I;
                create table %1$I.%3$I as select * from %2$I.%3$I limit 0;
                alter table %1$I.%3$I add column _data_valid_to timestamptz not null default now();
                $sql$,
                _history_schema, _record.table_schema, _record.table_name
            );
            raise info '%', replace(_command, '    ', '');
            execute _command;
        end if;

        -- add new after trigger
        _command = format(
            $sql$
            create or replace trigger %1$s
            after delete or update on %3$I.%4$I
            for each row execute procedure %2$s();
            $sql$,
            split_part(_trigger_name, '.', 2), _trigger_name, _record.table_schema, _record.table_name
        );

        raise info '%', replace(_command, '    ', '');
        execute _command;
    end loop;
end;
$$;