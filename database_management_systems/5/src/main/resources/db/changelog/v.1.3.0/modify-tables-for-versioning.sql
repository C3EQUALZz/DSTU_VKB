--liquibase formatted sql

--changeset DDD:260
ALTER TABLE posts
    ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);
--rollback ALTER TABLE posts DROP COLUMN sys_period;

--changeset DDD:261
ALTER TABLE masters_list
    ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);
--rollback ALTER TABLE masters_list DROP COLUMN sys_period;

--changeset DDD:262
ALTER TABLE orders_statuses
    ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);
--rollback ALTER TABLE orders_statuses DROP COLUMN sys_period;

--changeset DDD:263
ALTER TABLE equipments
    ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);
--rollback ALTER TABLE equipments DROP COLUMN sys_period;

--changeset DDD:264
ALTER TABLE clients
    ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);
--rollback ALTER TABLE clients DROP COLUMN sys_period;

--changeset DDD:265
ALTER TABLE components_warehouse
    ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);
--rollback ALTER TABLE components_warehouse DROP COLUMN sys_period;

--changeset DDD:266
ALTER TABLE order_executions
    ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);
--rollback ALTER TABLE order_executions DROP COLUMN sys_period;

--changeset DDD:267
ALTER TABLE components_order
    ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);
--rollback ALTER TABLE components_order DROP COLUMN sys_period;

--changeset DDD:268
ALTER TABLE orders
    ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);
--rollback ALTER TABLE orders DROP COLUMN sys_period;

--changeset DDD:269
CREATE TABLE posts_history (LIKE posts);
--rollback DROP TABLE posts_history IF EXISTS;

--changeset DDD:270
CREATE TABLE masters_list_history (LIKE masters_list);
--rollback DROP TABLE masters_list_history IF EXISTS;

--changeset DDD:271
CREATE TABLE orders_statuses_history (LIKE orders_statuses);
--rollback DROP TABLE orders_statuses_history IF EXISTS;

--changeset DDD:272
CREATE TABLE equipments_history (LIKE equipments);
--rollback DROP TABLE equipments_history IF EXISTS;

--changeset DDD:273
CREATE TABLE clients_history (LIKE clients);
--rollback DROP TABLE clients_history IF EXISTS;

--changeset DDD:274
CREATE TABLE components_warehouse_history (LIKE components_warehouse);
--rollback DROP TABLE components_warehouse_history IF EXISTS;

--changeset DDD:275
CREATE TABLE order_executions_history (LIKE order_executions);
--rollback DROP TABLE order_executions_history IF EXISTS;

--changeset DDD:276
CREATE TABLE components_order_history (LIKE components_order);
--rollback DROP TABLE components_order_history IF EXISTS;

--changeset DDD:277
CREATE TABLE orders_history (LIKE orders);
--rollback DROP TABLE orders_history IF EXISTS;