--liquibase formatted sql

--changeset DDD:278
CREATE TRIGGER versioning_trigger_posts
    BEFORE INSERT OR UPDATE OR DELETE ON posts
    FOR EACH ROW EXECUTE PROCEDURE versioning(
    'sys_period', 'posts_history', true
);
--rollback DROP TRIGGER IF EXISTS versioning_trigger_posts;

--changeset DDD:279
CREATE TRIGGER versioning_trigger_masters_list
    BEFORE INSERT OR UPDATE OR DELETE ON masters_list
    FOR EACH ROW EXECUTE PROCEDURE versioning(
    'sys_period', 'masters_list_history', true
);
--rollback DROP TRIGGER IF EXISTS versioning_trigger_masters_list;

--changeset DDD:280
CREATE TRIGGER versioning_trigger_orders_statuses
    BEFORE INSERT OR UPDATE OR DELETE ON orders_statuses
    FOR EACH ROW EXECUTE PROCEDURE versioning(
    'sys_period', 'orders_statuses_history', true
);
--rollback DROP TRIGGER IF EXISTS versioning_trigger_orders_statuses;

--changeset DDD:281
CREATE TRIGGER versioning_trigger_equipments
    BEFORE INSERT OR UPDATE OR DELETE ON equipments
    FOR EACH ROW EXECUTE PROCEDURE versioning(
    'sys_period', 'equipments_history', true
);
--rollback DROP TRIGGER IF EXISTS versioning_trigger_equipments;

--changeset DDD:282
CREATE TRIGGER versioning_trigger_clients
    BEFORE INSERT OR UPDATE OR DELETE ON clients
    FOR EACH ROW EXECUTE PROCEDURE versioning(
    'sys_period', 'clients_history', true
);
--rollback DROP TRIGGER IF EXISTS versioning_trigger_clients;

--changeset DDD:283
CREATE TRIGGER versioning_trigger_components_warehouse
    BEFORE INSERT OR UPDATE OR DELETE ON components_warehouse
    FOR EACH ROW EXECUTE PROCEDURE versioning(
    'sys_period', 'components_warehouse_history', true
);
--rollback DROP TRIGGER IF EXISTS versioning_trigger_components_warehouse;

--changeset DDD:284
CREATE TRIGGER versioning_trigger_order_executions
    BEFORE INSERT OR UPDATE OR DELETE ON order_executions
    FOR EACH ROW EXECUTE PROCEDURE versioning(
    'sys_period', 'order_executions_history', true
);
--rollback DROP TRIGGER IF EXISTS versioning_trigger_order_executions;

--changeset DDD:285
CREATE TRIGGER versioning_trigger_components_order
    BEFORE INSERT OR UPDATE OR DELETE ON components_order
    FOR EACH ROW EXECUTE PROCEDURE versioning(
    'sys_period', 'components_order_history', true
);
--rollback DROP TRIGGER IF EXISTS versioning_trigger_components_order;

--changeset DDD:286
CREATE TRIGGER versioning_trigger_orders
    BEFORE INSERT OR UPDATE OR DELETE ON orders
    FOR EACH ROW EXECUTE PROCEDURE versioning(
    'sys_period', 'orders_history', true
);
--rollback DROP TRIGGER IF EXISTS versioning_trigger_orders;

