import ast

from app.utils.crypto import pg_scram_sha256
from app.utils.decorators import database_required, user_authenticated
from django.http import HttpResponse, JsonResponse

@user_authenticated
@database_required(check_timeout=True, open_connection=True, prefer_database='postgres')
def get_tree_info(request, database):
    try:
        data = {
            "database": database.GetName(),
            "version": database.GetVersion(),
            #'superuser': database.GetUserSuper(),
            "drop_role": database.TemplateDropRole().v_text,
            "create_tablespace": database.TemplateCreateTablespace().v_text,
            "alter_tablespace": database.TemplateAlterTablespace().v_text,
            "drop_tablespace": database.TemplateDropTablespace().v_text,
            "create_database": database.TemplateCreateDatabase().v_text,
            "alter_database": database.TemplateAlterDatabase().v_text,
            "drop_database": database.TemplateDropDatabase().v_text,
            "create_schema": database.TemplateCreateSchema().v_text,
            "alter_schema": database.TemplateAlterSchema().v_text,
            "drop_schema": database.TemplateDropSchema().v_text,
            "create_sequence": database.TemplateCreateSequence().v_text,
            "alter_sequence": database.TemplateAlterSequence().v_text,
            "drop_sequence": database.TemplateDropSequence().v_text,
            "create_function": database.TemplateCreateFunction().v_text,
            "alter_function": database.TemplateAlterFunction().v_text,
            "drop_function": database.TemplateDropFunction().v_text,
            "create_procedure": database.TemplateCreateProcedure().v_text,
            "alter_procedure": database.TemplateAlterProcedure().v_text,
            "drop_procedure": database.TemplateDropProcedure().v_text,
            "create_triggerfunction": database.TemplateCreateTriggerFunction().v_text,
            "alter_triggerfunction": database.TemplateAlterTriggerFunction().v_text,
            "drop_triggerfunction": database.TemplateDropTriggerFunction().v_text,
            "create_eventtriggerfunction": database.TemplateCreateEventTriggerFunction().v_text,
            "alter_eventtriggerfunction": database.TemplateAlterEventTriggerFunction().v_text,
            "drop_eventtriggerfunction": database.TemplateDropEventTriggerFunction().v_text,
            "create_aggregate": database.TemplateCreateAggregate().v_text,
            "alter_aggregate": database.TemplateAlterAggregate().v_text,
            "drop_aggregate": database.TemplateDropAggregate().v_text,
            "create_view": database.TemplateCreateView().v_text,
            "alter_view": database.TemplateAlterView().v_text,
            "drop_view": database.TemplateDropView().v_text,
            "create_mview": database.TemplateCreateMaterializedView().v_text,
            "refresh_mview": database.TemplateRefreshMaterializedView().v_text,
            "alter_mview": database.TemplateAlterMaterializedView().v_text,
            "drop_mview": database.TemplateDropMaterializedView().v_text,
            "drop_table": database.TemplateDropTable().v_text,
            "create_column": database.TemplateCreateColumn().v_text,
            "alter_column": database.TemplateAlterColumn().v_text,
            "drop_column": database.TemplateDropColumn().v_text,
            "create_primarykey": database.TemplateCreatePrimaryKey().v_text,
            "drop_primarykey": database.TemplateDropPrimaryKey().v_text,
            "create_unique": database.TemplateCreateUnique().v_text,
            "drop_unique": database.TemplateDropUnique().v_text,
            "create_foreignkey": database.TemplateCreateForeignKey().v_text,
            "drop_foreignkey": database.TemplateDropForeignKey().v_text,
            "create_index": database.TemplateCreateIndex().v_text,
            "alter_index": database.TemplateAlterIndex().v_text,
            "cluster_index": database.TemplateClusterIndex().v_text,
            "reindex": database.TemplateReindex().v_text,
            "drop_index": database.TemplateDropIndex().v_text,
            "create_check": database.TemplateCreateCheck().v_text,
            "drop_check": database.TemplateDropCheck().v_text,
            "create_exclude": database.TemplateCreateExclude().v_text,
            "drop_exclude": database.TemplateDropExclude().v_text,
            "create_rule": database.TemplateCreateRule().v_text,
            "alter_rule": database.TemplateAlterRule().v_text,
            "drop_rule": database.TemplateDropRule().v_text,
            "create_trigger": database.TemplateCreateTrigger().v_text,
            "create_view_trigger": database.TemplateCreateViewTrigger().v_text,
            "alter_trigger": database.TemplateAlterTrigger().v_text,
            "enable_trigger": database.TemplateEnableTrigger().v_text,
            "disable_trigger": database.TemplateDisableTrigger().v_text,
            "drop_trigger": database.TemplateDropTrigger().v_text,
            "create_eventtrigger": database.TemplateCreateEventTrigger().v_text,
            "alter_eventtrigger": database.TemplateAlterEventTrigger().v_text,
            "enable_eventtrigger": database.TemplateEnableEventTrigger().v_text,
            "disable_eventtrigger": database.TemplateDisableEventTrigger().v_text,
            "drop_eventtrigger": database.TemplateDropEventTrigger().v_text,
            "create_inherited": database.TemplateCreateInherited().v_text,
            "noinherit_partition": database.TemplateNoInheritPartition().v_text,
            "create_partition": database.TemplateCreatePartition().v_text,
            "detach_partition": database.TemplateDetachPartition().v_text,
            "drop_partition": database.TemplateDropPartition().v_text,
            "vacuum": database.TemplateVacuum().v_text,
            "vacuum_table": database.TemplateVacuumTable().v_text,
            "analyze": database.TemplateAnalyze().v_text,
            "analyze_table": database.TemplateAnalyzeTable().v_text,
            "delete": database.TemplateDelete().v_text,
            "truncate": database.TemplateTruncate().v_text,
            "create_physicalreplicationslot": database.TemplateCreatePhysicalReplicationSlot().v_text,
            "drop_physicalreplicationslot": database.TemplateDropPhysicalReplicationSlot().v_text,
            "create_logicalreplicationslot": database.TemplateCreateLogicalReplicationSlot().v_text,
            "drop_logicalreplicationslot": database.TemplateDropLogicalReplicationSlot().v_text,
            "create_publication": database.TemplateCreatePublication().v_text,
            "alter_publication": database.TemplateAlterPublication().v_text,
            "drop_publication": database.TemplateDropPublication().v_text,
            "add_pubtable": database.TemplateAddPublicationTable().v_text,
            "drop_pubtable": database.TemplateDropPublicationTable().v_text,
            "create_subscription": database.TemplateCreateSubscription().v_text,
            "alter_subscription": database.TemplateAlterSubscription().v_text,
            "drop_subscription": database.TemplateDropSubscription().v_text,
            "create_fdw": database.TemplateCreateForeignDataWrapper().v_text,
            "alter_fdw": database.TemplateAlterForeignDataWrapper().v_text,
            "drop_fdw": database.TemplateDropForeignDataWrapper().v_text,
            "create_foreign_server": database.TemplateCreateForeignServer().v_text,
            "alter_foreign_server": database.TemplateAlterForeignServer().v_text,
            "import_foreign_schema": database.TemplateImportForeignSchema().v_text,
            "drop_foreign_server": database.TemplateDropForeignServer().v_text,
            "create_foreign_table": database.TemplateCreateForeignTable().v_text,
            "alter_foreign_table": database.TemplateAlterForeignTable().v_text,
            "drop_foreign_table": database.TemplateDropForeignTable().v_text,
            "create_foreign_column": database.TemplateCreateForeignColumn().v_text,
            "alter_foreign_column": database.TemplateAlterForeignColumn().v_text,
            "drop_foreign_column": database.TemplateDropForeignColumn().v_text,
            "create_user_mapping": database.TemplateCreateUserMapping().v_text,
            "alter_user_mapping": database.TemplateAlterUserMapping().v_text,
            "drop_user_mapping": database.TemplateDropUserMapping().v_text,
            "create_type": database.TemplateCreateType().v_text,
            "alter_type": database.TemplateAlterType().v_text,
            "drop_type": database.TemplateDropType().v_text,
            "create_domain": database.TemplateCreateDomain().v_text,
            "alter_domain": database.TemplateAlterDomain().v_text,
            "drop_domain": database.TemplateDropDomain().v_text,
            "create_statistics": database.TemplateCreateStatistics().v_text,
            "alter_statistics": database.TemplateAlterStatistics().v_text,
            "drop_statistics": database.TemplateDropStatistics().v_text,
            "has_replication_slots": database.has_replication_slots,
        }
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=data)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_database_objects(request, database):
    unsupported_versions = ["1.0", "1.1", "1.2", "1.3"]
    version_filter = (
        lambda extension: extension[0] == "pg_cron"
        and extension[2] not in unsupported_versions
    )
    has_pg_cron = False
    try:
        current_schema = "public"
        schema = database.QueryCurrentSchema().Rows
        if schema:
            [current_schema] = schema[0]
        if database.has_extensions:
            extensions = database.QueryExtensions().Rows
            has_pg_cron = len(list(filter(version_filter, extensions))) > 0
        data = {
            "has_extensions": database.has_extensions,
            "has_fdw": database.has_fdw,
            "has_event_triggers": database.has_event_triggers,
            "has_logical_replication": database.has_logical_replication,
            "has_pg_cron": has_pg_cron,
            "current_schema": current_schema
            }
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=data)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_properties(request, database):
    data = request.data["data"]

    list_properties = []
    ddl = ""

    try:
        properties = database.GetProperties(
            data["schema"], data["table"], data["object"], data["type"]
        )
        for property_object in properties.Rows:
            list_properties.append(
                [property_object["Property"], property_object["Value"]]
            )
        ddl = database.GetDDL(
            data["schema"], data["table"], data["object"], data["type"]
        )
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"properties": list_properties, "ddl": ddl})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_tables(request, database):
    schema = request.data["schema"]

    list_tables = []

    try:
        tables = database.QueryTables(False, schema)
        for table in tables.Rows:
            table_data = {
                "name": table["table_name"],
                "oid": table["oid"],
                "name_raw": table["name_raw"],
            }
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_columns(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_columns = []

    try:
        columns = database.QueryTablesFields(table, False, schema)
        for column in columns.Rows:
            column_data = {
                "column_name": column["column_name"],
                "name_raw": column["name_raw"],
                "data_type": column["data_type"],
                "data_length": column["data_length"],
                "nullable": column["nullable"],
                "position": column["position"],
            }
            list_columns.append(column_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_columns, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_table_definition(request, v_database):
    data = request.data
    columns = []
    try:
        table = data["table"]
        schema = data["schema"]

        q_primaries = v_database.QueryTablePKColumns(table, schema)
        pk_column_names = [x[0] for x in q_primaries.Rows]
        q_definition = v_database.QueryTableDefinition(table, schema)
        for col in q_definition.Rows:
            column_data = {
                "name": col["column_name"],
                "data_type": col["data_type"],
                "default_value": col["column_default"],
                "nullable": col["is_nullable"] != "NO",
                "is_primary": col["column_name"] in pk_column_names,
                "comment": col["comment"],
            }
            columns.append(column_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": columns})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_pk(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_pk = []

    try:
        pks = database.QueryTablesPrimaryKeys(table, False, schema)
        for pk in pks.Rows:
            pk_data = {
                "constraint_name": pk["constraint_name"],
                "oid": pk["oid"],
                "name_raw": pk["name_raw"],
            }
            list_pk.append(pk_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_pk, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_pk_columns(request, database):
    data = request.data
    pkey = data["key"]
    table = data["table"]
    schema = data["schema"]

    try:
        pks = database.QueryTablesPrimaryKeysColumns(pkey, table, False, schema)
        list_pk = [pk["column_name"] for pk in pks.Rows]
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_pk, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_fks(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_fk = []

    try:
        fks = database.QueryTablesForeignKeys(table, False, schema)
        for fk in fks.Rows:
            fk_data = {
                "constraint_name": fk["constraint_name"],
                "oid": fk["oid"],
                "name_raw": fk["name_raw"],
            }
            list_fk.append(fk_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_fk, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_fks_columns(request, database):
    data = request.data
    fkey = data["fkey"]
    table = data["table"]
    schema = data["schema"]

    list_fk = []

    try:
        fks = database.QueryTablesForeignKeysColumns(fkey, table, False, schema)
        for fk in fks.Rows:
            fk_data = {
                "r_table_name": fk["r_table_name"],
                "delete_rule": fk["delete_rule"],
                "update_rule": fk["update_rule"],
                "column_name": fk["column_name"],
                "r_column_name": fk["r_column_name"],
            }
            list_fk.append(fk_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_fk, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_uniques(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_uniques = []

    try:
        uniques = database.QueryTablesUniques(table, False, schema)
        for unique in uniques.Rows:
            v_unique_data = {
                "constraint_name": unique["constraint_name"],
                "oid": unique["oid"],
                "name_raw": unique["name_raw"],
            }
            list_uniques.append(v_unique_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_uniques, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_uniques_columns(request, database):
    data = request.data
    unique = data["unique"]
    table = data["table"]
    schema = data["schema"]

    try:
        uniques = database.QueryTablesUniquesColumns(unique, table, False, schema)
        list_uniques = [unique["column_name"] for unique in uniques.Rows]
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_uniques, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_indexes(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_indexes = []

    try:
        indexes = database.QueryTablesIndexes(table, False, schema)
        for index in indexes.Rows:
            index_data = {
                "index_name": index["index_name"],
                "name_raw": index["name_raw"],
                "unique": index["uniqueness"] == "Unique",
                "type": "unique" if index["uniqueness"] == "Unique" else "non-unique",
                "oid": index["oid"],
                "is_primary": index["is_primary"] == "True",
                "columns": list(ast.literal_eval(index["columns"])),
                "method": index["method"],
                "predicate": index["constraint"],
            }
            list_indexes.append(index_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_indexes, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_indexes_columns(request, database):
    data = request.data
    index = data["index"]
    table = data["table"]
    schema = data["schema"]

    try:
        indexes = database.QueryTablesIndexesColumns(index, table, False, schema)
        list_indexes = [index["column_name"] for index in indexes.Rows]
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_indexes, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_checks(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_checks = []

    try:
        checks = database.QueryTablesChecks(table, False, schema)
        for check in checks.Rows:
            check_data = {
                "constraint_name": check["constraint_name"],
                "name_raw": check["name_raw"],
                "constraint_source": check["constraint_source"],
                "oid": check["oid"],
            }
            list_checks.append(check_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_checks, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_excludes(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_excludes = []

    try:
        excludes = database.QueryTablesExcludes(table, False, schema)
        for exclude in excludes.Rows:
            exclude_data = {
                "constraint_name": exclude["constraint_name"],
                "name_raw": exclude["name_raw"],
                "attributes": exclude["attributes"],
                "operations": exclude["operations"],
                "oid": exclude["oid"],
            }
            list_excludes.append(exclude_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_excludes, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_rules(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_rules = []

    try:
        rules = database.QueryTablesRules(table, False, schema)
        for rule in rules.Rows:
            rule_data = {
                "rule_name": rule["rule_name"],
                "oid": rule["oid"],
                "name_raw": rule["name_raw"],
            }
            list_rules.append(rule_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_rules, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_rule_definition(request, database):
    data = request.data
    rule = data["rule"]
    table = data["table"]
    schema = data["schema"]

    try:
        rule_definition = database.GetRuleDefinition(rule, table, schema)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": rule_definition})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_triggers(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_triggers = []

    try:
        triggers = database.QueryTablesTriggers(table, False, schema)
        for trigger in triggers.Rows:
            trigger_data = {
                "trigger_name": trigger["trigger_name"],
                "name_raw": trigger["name_raw"],
                "enabled": trigger["trigger_enabled"],
                "trigger_function": trigger["trigger_function"],
                "id": trigger["id"],
                "function_oid": trigger["function_oid"],
                "oid": trigger["oid"],
            }
            list_triggers.append(trigger_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_triggers, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_eventtriggers(request, database):
    list_triggers = []

    try:
        triggers = database.QueryEventTriggers()
        for trigger in triggers.Rows:
            trigger_data = {
                "name": trigger["trigger_name"],
                "name_raw": trigger["name_raw"],
                "enabled": trigger["trigger_enabled"],
                "event": trigger["event_name"],
                "function": trigger["trigger_function"],
                "id": trigger["id"],
                "function_oid": trigger["function_oid"],
                "oid": trigger["oid"],
            }
            list_triggers.append(trigger_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_triggers, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_inheriteds(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    try:
        partitions = database.QueryTablesInheriteds(table, False, schema)
        list_partitions = [
            f'{partition["child_schema"]}.{partition["child_table"]}'
            for partition in partitions.Rows
        ]
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_partitions, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_partitions(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    try:
        partitions = database.QueryTablesPartitions(table, False, schema)
        list_partitions = [
            partition["child_table"] for partition in partitions.Rows
        ]
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_partitions, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_statistics(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_statistics = []

    try:
        statistics = database.QueryTablesStatistics(table, False, schema)
        for statistic in statistics.Rows:
            statistic_data = {
                "statistic_name": statistic["statistic_name"],
                "name_raw": statistic["name_raw"],
                "schema_name": statistic["schema_name"],
                "oid": statistic["oid"],
            }
            list_statistics.append(statistic_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_statistics, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_statistics_columns(request, database):
    data = request.data
    statistics = data["statistics"]
    schema = data["schema"]

    list_columns = []

    try:
        columns = database.QueryStatisticsFields(statistics, False, schema)
        for column in columns.Rows:
            column_data = {"column_name": column["column_name"]}
            list_columns.append(column_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_columns, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_views(request, database):
    schema = request.data["schema"]

    list_tables = []

    try:
        tables = database.QueryViews(False, schema)
        for table in tables.Rows:
            table_data = {
                "name": table["table_name"],
                "oid": table["oid"],
                "name_raw": table["name_raw"],
            }
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_views_columns(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_columns = []

    try:
        columns = database.QueryViewFields(table, False, schema)
        for column in columns.Rows:
            column_data = {
                "column_name": column["column_name"],
                "name_raw": column["name_raw"],
                "data_type": column["data_type"],
            }
            list_columns.append(column_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_columns, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_view_definition(request, database):
    data = request.data
    view = data["view"]
    schema = data["schema"]

    try:
        view_definition = database.GetViewDefinition(view, schema)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": view_definition})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_mviews(request, database):
    schema = request.data["schema"]

    list_tables = []

    try:
        tables = database.QueryMaterializedViews(False, schema)
        for table in tables.Rows:
            table_data = {
                "name": table["table_name"],
                "oid": table["oid"],
                "name_raw": table["name_raw"],
            }
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_mviews_columns(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_columns = []

    try:
        columns = database.QueryMaterializedViewFields(table, False, schema)
        for column in columns.Rows:
            column_data = {
                "column_name": column["column_name"],
                "name_raw": column["name_raw"],
                "data_type": column["data_type"],
            }
            list_columns.append(column_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_columns, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_mview_definition(request, database):
    data = request.data
    view = data["view"]
    schema = data["schema"]

    try:
        mview_definition = database.GetMaterializedViewDefinition(view, schema)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": mview_definition})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_schemas(request, database):
    schemas_list = []

    try:
        schemas = database.QuerySchemas()
        for schema in schemas.Rows:
            schema_data = {
                "name": schema["schema_name"],
                "oid": schema["oid"],
                "name_raw": schema["name_raw"],
            }
            schemas_list.append(schema_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=500)
    return JsonResponse(data=schemas_list, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True, prefer_database='postgres')
def get_databases(request, database):
    list_databases = []

    try:
        databases = database.QueryDatabases()
        for database_object in databases.Rows:
            database_data = {
                "name": database_object["database_name"],
                "name_raw": database_object["name_raw"],
                "oid": database_object["oid"],
            }
            list_databases.append(database_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_databases, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_tablespaces(request, database):
    list_tablespaces = []

    try:
        tablespaces = database.QueryTablespaces()
        for tablespace in tablespaces.Rows:
            tablespace_data = {
                "name": tablespace["tablespace_name"],
                "oid": tablespace["oid"],
            }
            list_tablespaces.append(tablespace_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)
    return JsonResponse(data=list_tablespaces, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_roles(request, database):
    list_roles = []
    try:
        roles = database.QueryRoles()
        for role in roles.Rows:
            role_data = {
                "name": role["role_name"],
                "oid": role["oid"],
                "name_raw": role["name_raw"],
            }
            list_roles.append(role_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)
    return JsonResponse(data={"data": list_roles})

@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_role_details(request, database):
    role_oid = request.data["oid"]

    try:
        role = database.QueryRoleDetails(role_oid)
        if not role.Rows:
            return JsonResponse(
                {"data": f"Role with oid '{role_oid}' does not exist."}, status=400
            )

        rolerow = role.Rows[0]

        role_details = {
            'name': rolerow["role_name"],
            'name_raw': rolerow["name_raw"],
            'rolsuper': rolerow["rolsuper"],
            'rolinherit': rolerow["rolinherit"],
            'rolcanlogin': rolerow["rolcanlogin"],
            'rolcreaterole': rolerow["rolcreaterole"],
            'rolcreatedb': rolerow["rolcreatedb"],
            'rolbypassrls': rolerow["rolbypassrls"],
            'rolreplication': rolerow["rolreplication"],
            'rolconnlimit': rolerow["rolconnlimit"],
            'rolpassword': rolerow["rolpassword"],
            'rolvaliduntil': None if rolerow["rolvaliduntil"] == 'infinity' else rolerow["rolvaliduntil"],
            'members': rolerow["members"],
            'member_of': rolerow["member_of"],
        }

    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)


    return JsonResponse(data=role_details)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_functions(request, database):
    schema = request.data["schema"]

    list_functions = []

    try:
        functions = database.QueryFunctions(False, schema)
        for function in functions.Rows:
            function_data = {
                "name": function["name"],
                "name_raw": function["name_raw"],
                "id": function["id"],
                "function_oid": function["function_oid"],
            }
            list_functions.append(function_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_functions, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_function_fields(request, database):
    data = request.data
    function = data["function"]
    schema = data["schema"]

    list_fields = []

    try:
        fields = database.QueryFunctionFields(function, schema)
        for field in fields.Rows:
            field_data = {"name": field["name"], "type": field["type"]}
            list_fields.append(field_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_fields, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_function_definition(request, database):
    function = request.data["function"]

    try:
        function_definition = database.GetFunctionDefinition(function)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": function_definition})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_function_debug(request, database):
    function = request.data["function"]

    try:
        response_data = database.GetFunctionDebug(function)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": response_data})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_procedures(request, database):
    schema = request.data["schema"]

    list_functions = []

    try:
        functions = database.QueryProcedures(False, schema)
        for function in functions.Rows:
            function_data = {
                "name": function["name"],
                "id": function["id"],
                "function_oid": function["function_oid"],
            }
            list_functions.append(function_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_functions, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_procedure_fields(request, database):
    data = request.data
    function = data["procedure"]
    schema = data["schema"]

    list_fields = []

    try:
        fields = database.QueryProcedureFields(function, schema)
        for field in fields.Rows:
            field_data = {"name": field["name"], "type": field["type"]}
            list_fields.append(field_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_fields, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_procedure_definition(request, database):
    function = request.data["procedure"]

    try:
        procedure_definition = database.GetProcedureDefinition(function)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": procedure_definition})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_procedure_debug(request, database):
    function = request.data["procedure"]

    try:
        response_data = database.GetProcedureDebug(function)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": response_data})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_triggerfunctions(request, database):
    schema = request.data["schema"]

    list_functions = []

    try:
        functions = database.QueryTriggerFunctions(False, schema)
        for function in functions.Rows:
            function_data = {
                "name": function["name"],
                "id": function["id"],
                "function_oid": function["function_oid"],
            }
            list_functions.append(function_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_functions, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_triggerfunction_definition(request, database):
    function = request.data["function"]

    try:
        trigger_function_definition = database.GetTriggerFunctionDefinition(function)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": trigger_function_definition})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_eventtriggerfunctions(request, database):
    schema = request.data["schema"]

    list_functions = []

    try:
        functions = database.QueryEventTriggerFunctions(False, schema)
        for function in functions.Rows:
            function_data = {
                "name": function["name"],
                "id": function["id"],
                "function_oid": function["function_oid"],
            }
            list_functions.append(function_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_functions, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_eventtriggerfunction_definition(request, database):
    function = request.data["function"]

    try:
        function_definition = database.GetEventTriggerFunctionDefinition(function)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": function_definition})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_aggregates(request, database):
    schema = request.data["schema"]

    list_aggregates = []

    try:
        aggregates = database.QueryAggregates(False, schema)
        for aggregate in aggregates.Rows:
            aggregate_data = {
                "name": aggregate["name"],
                "id": aggregate["id"],
                "oid": aggregate["oid"],
            }
            list_aggregates.append(aggregate_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_aggregates, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_sequences(request, database):
    schema = request.data["schema"]

    list_sequences = []

    try:
        sequences = database.QuerySequences(False, schema)
        for sequence in sequences.Rows:
            sequence_data = {
                "sequence_name": sequence["sequence_name"],
                "name_raw": sequence["name_raw"],
                "oid": sequence["oid"],
            }
            list_sequences.append(sequence_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_sequences, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_extensions(request, database):
    list_extensions = []

    try:
        extensions = database.QueryExtensions()
        for extension in extensions.Rows:
            extension_data = {
                "name": extension["extension_name"],
                "name_raw": extension["name_raw"],
                "oid": extension["oid"],
            }
            list_extensions.append(extension_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_extensions, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_available_extensions(request, database):
    available_extensions = database.QueryAvailableExtensionsVersions()

    list_ext = []

    for extension in available_extensions.Rows:
        extension_data = {
            "name": extension["name"],
            "versions": extension["versions"],
            "comment": extension["comment"],
            "required_schema": extension["required_schema"],
        }
        list_ext.append(extension_data)
    return JsonResponse({"available_extensions": list_ext})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_extension_details(request, database):
    data = request.data

    extension = database.QueryExtensionByName(data.get("ext_name"))

    if not extension.Rows:
        return JsonResponse(
            {"data": f"Extension '{data.get('ext_name')}' does not exist."}, status=400
        )

    [extension_detail] = extension.Rows

    return JsonResponse(data=dict(extension_detail))


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def execute_query(request, database):
    data = request.data
    try:
        database.Execute(data.get("query"))
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)
    return JsonResponse({"status": "success"})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_physicalreplicationslots(request, database):
    list_repslots = []

    try:
        repslots = database.QueryPhysicalReplicationSlots()
        for repslot in repslots.Rows:
            repslot_data = {"name": repslot["slot_name"]}
            list_repslots.append(repslot_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)
    return JsonResponse(data=list_repslots, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_logicalreplicationslots(request, database):
    list_repslots = []

    try:
        repslots = database.QueryLogicalReplicationSlots()
        for repslot in repslots.Rows:
            repslot_data = {"name": repslot["slot_name"]}
            list_repslots.append(repslot_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)
    return JsonResponse(data=list_repslots, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_publications(request, database):
    list_pubs = []

    try:
        pubs = database.QueryPublications()
        for pub in pubs.Rows:
            pub_data = {
                "name": pub["pubname"],
                "name_raw": pub["name_raw"],
                "alltables": pub["puballtables"],
                "insert": pub["pubinsert"],
                "update": pub["pubupdate"],
                "delete": pub["pubdelete"],
                "truncate": pub["pubtruncate"],
                "oid": pub["oid"],
            }
            list_pubs.append(pub_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_pubs, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_publication_tables(request, database):
    pub = request.data["pub"]

    list_tables = []

    try:
        tables = database.QueryPublicationTables(pub)
        for table in tables.Rows:
            table_data = {"name": table["table_name"]}
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_subscriptions(request, database):
    list_subs = []

    try:
        subs = database.QuerySubscriptions()
        for sub in subs.Rows:
            sub_data = {
                "name": sub["subname"],
                "name_raw": sub["name_raw"],
                "enabled": sub["subenabled"],
                "conn_info": sub["subconninfo"],
                "publications": sub["subpublications"],
                "oid": sub["oid"],
            }
            list_subs.append(sub_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_subs, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_subscription_tables(request, database):
    sub = request.data["sub"]

    list_tables = []

    try:
        tables = database.QuerySubscriptionTables(sub)
        for table in tables.Rows:
            table_data = {"name": table["table_name"]}
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_foreign_data_wrappers(request, database):
    list_fdws = []

    try:
        fdws = database.QueryForeignDataWrappers()
        for fdw in fdws.Rows:
            fdw_data = {"name": fdw["fdwname"], "oid": fdw["oid"]}
            list_fdws.append(fdw_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_fdws, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_foreign_servers(request, database):
    fdw = request.data["fdw"]

    list_servers = []

    try:
        servers = database.QueryForeignServers(fdw)
        for server in servers.Rows:
            server_data = {
                "name": server["srvname"],
                "name_raw": server["name_raw"],
                "type": server["srvtype"],
                "version": server["srvversion"],
                "options": server["srvoptions"],
                "oid": server["oid"],
            }
            list_servers.append(server_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_servers, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_user_mappings(request, database):
    foreign_server = request.data["foreign_server"]

    list_mappings = []

    try:
        mappings = database.QueryUserMappings(foreign_server)
        for mapping in mappings.Rows:
            mapping_data = {
                "name": mapping["rolname"],
                "name_raw": mapping["name_raw"],
                "options": mapping["umoptions"],
                "foreign_server": foreign_server,
            }
            list_mappings.append(mapping_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_mappings, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_foreign_tables(request, database):
    schema = request.data["schema"]

    list_tables = []

    try:
        tables = database.QueryForeignTables(False, schema)
        for table in tables.Rows:
            table_data = {
                "name": table["table_name"],
                "oid": table["oid"],
                "name_raw": table["name_raw"],
            }
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_foreign_columns(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_columns = []

    try:
        columns = database.QueryForeignTablesFields(table, False, schema)
        for column in columns.Rows:
            column_data = {
                "column_name": column["column_name"],
                "data_type": column["data_type"],
                "data_length": column["data_length"],
                "nullable": column["nullable"],
                "options": column["attfdwoptions"],
                "table_options": column["ftoptions"],
                "server": column["srvname"],
                "fdw": column["fdwname"],
            }
            list_columns.append(column_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_columns, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_types(request, database):
    schema = request.data["schema"]

    list_types = []

    try:
        types = database.QueryTypes(False, schema)
        for type_object in types.Rows:
            type_data = {
                "type_name": type_object["type_name"],
                "name_raw": type_object["name_raw"],
                "oid": type_object["oid"],
            }
            list_types.append(type_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_types, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_domains(request, database):
    schema = request.data["schema"]

    list_domains = []

    try:
        domains = database.QueryDomains(False, schema)
        for domain in domains.Rows:
            domain_data = {
                "domain_name": domain["domain_name"],
                "oid": domain["oid"],
                "name_raw": domain["name_raw"],
            }
            list_domains.append(domain_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_domains, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_inheriteds_parents(request, database):
    schema = request.data["schema"]

    list_tables = []
    try:
        tables = database.QueryTablesInheritedsParents(False, schema)
        for table in tables.Rows:
            table_data = {
                "name": f'{table["table_schema"]}.{table["table_name"]}',
                "name_raw": f'{table["table_schema_raw"]}.{table["name_raw"]}',
            }
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_inheriteds_children(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_tables = []

    try:
        tables = database.QueryTablesInheritedsChildren(table, schema)
        for table in tables.Rows:
            table_data = {
                "name": table["table_name"],
                "oid": table["oid"],
                "name_raw": table["name_raw"],
            }
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_partitions_parents(request, database):
    schema = request.data["schema"]

    list_tables = []
    try:
        tables = database.QueryTablesPartitionsParents(False, schema)
        for table in tables.Rows:
            table_data = {
                "name": table["table_name"],
                "name_raw": f'{table["table_schema_raw"]}.{table["name_raw"]}',
            }
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_partitions_children(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    list_tables = []

    try:
        tables = database.QueryTablesPartitionsChildren(table, schema)
        for table in tables.Rows:
            table_data = {
                "name": table["table_name"],
                "oid": table["oid"],
                "name_raw": table["name_raw"],
            }
            list_tables.append(table_data)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=list_tables, safe=False)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def kill_backend(request, database):
    pid = request.data["pid"]

    try:
        database.Terminate(pid)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return HttpResponse(status=204)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def template_select(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]
    kind = data["kind"]

    try:
        template = database.TemplateSelect(schema, table, kind).v_text
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"template": template})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def template_insert(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    try:
        template = database.TemplateInsert(schema, table).v_text
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"template": template})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def template_update(request, database):
    data = request.data
    table = data["table"]
    schema = data["schema"]

    try:
        template = database.TemplateUpdate(schema, table).v_text
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"template": template})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def template_select_function(request, database):
    data = request.data
    function = data["function"]
    functionid = data["functionid"]
    schema = data["schema"]

    try:
        template = database.TemplateSelectFunction(schema, function, functionid).v_text
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"template": template})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def template_call_procedure(request, database):
    data = request.data
    procedure = data["procedure"]
    procedureid = data["procedureid"]
    schema = data["schema"]

    try:
        template = database.TemplateCallProcedure(schema, procedure, procedureid).v_text
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"template": template})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_version(request, database):
    try:
        response_data = {"version": database.GetVersion()}
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data=response_data)


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def change_role_password(request, database):
    data = request.data

    password = data["password"]

    hashed_password = pg_scram_sha256(password)

    try:
        database.ChangeRolePassword(data["role"], hashed_password)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse({"status": "success"})


@user_authenticated
@database_required(check_timeout=True, open_connection=True)
def get_object_description(request, database):
    data = request.data
    oid = data["oid"]
    object_type = data["object_type"]
    position = data["position"]

    try:
        object_description = database.GetObjectDescription(object_type, oid, position)
    except Exception as exc:
        return JsonResponse(data={"data": str(exc)}, status=400)

    return JsonResponse(data={"data": object_description})
