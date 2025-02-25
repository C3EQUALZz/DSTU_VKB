--liquibase formatted sql

--changeset DDD:1.0.1
CREATE TABLE posts
(
    post_code UUID PRIMARY KEY,
    post_name VARCHAR(50) NOT NULL UNIQUE
);

--changeset DDD:1.0.2
CREATE TABLE masters_list
(
    master_code        UUID PRIMARY KEY,
    post_code          UUID         NOT NULL,
    surname            VARCHAR(30)  NOT NULL,
    name               VARCHAR(30)  NOT NULL,
    patronymic         VARCHAR(30)  NOT NULL,
    address            VARCHAR(100) NOT NULL,
    phone_number       VARCHAR      NOT NULL,
    date_of_employment DATE         NOT NULL CHECK (date_of_employment > '1980-01-01')
);

--changeset DDD:1.0.3
CREATE TABLE orders_statuses
(
    status_code UUID PRIMARY KEY,
    status_name VARCHAR(30) NOT NULL UNIQUE
);

--changeset DDD:1.0.4
CREATE TABLE equipments
(
    eq_code          UUID PRIMARY KEY,
    eq_name          VARCHAR(50) NOT NULL,
    eq_serial_number VARCHAR     NOT NULL,
    model            VARCHAR(50) NOT NULL
);

--changeset DDD:1.0.5
CREATE TABLE clients
(
    client_code  UUID PRIMARY KEY,
    surname      VARCHAR(30) NOT NULL,
    name         VARCHAR(30) NOT NULL,
    patronymic   VARCHAR(30) NOT NULL,
    phone_number VARCHAR     NOT NULL,
    email        VARCHAR     NOT NULL UNIQUE,
    password     VARCHAR     NOT NULL,
    role         VARCHAR     DEFAULT 'USER'
);

--changeset DDD:1.0.6
CREATE TABLE components_warehouse
(
    components_code   UUID PRIMARY KEY,
    component_name    VARCHAR(50) NOT NULL,
    components_amount INTEGER     NOT NULL,
    unit_cost         DECIMAL     NOT NULL
);

--changeset DDD:1.0.7
CREATE TABLE order_executions
(
    ex_code         UUID PRIMARY KEY,
    type_of_work    VARCHAR(50)    NOT NULL,
    ex_cost         DECIMAL(10, 2) NOT NULL,
    components_cost DECIMAL(10, 2),
    ex_date         DATE           NOT NULL CHECK (ex_date > '1980-01-01')
);

--changeset DDD:1.0.8
ALTER TABLE order_executions
    ADD COLUMN total_cost DECIMAL(10, 2) GENERATED ALWAYS AS (ex_cost + COALESCE(components_cost, 0)) STORED;

--changeset DDD:1.0.9
CREATE TABLE components_order
(
    co_code        UUID PRIMARY KEY,
    component_code UUID NOT NULL,
    execution_code UUID NOT NULL
);

--changeset DDD:1.0.10
CREATE TABLE orders
(
    order_code            UUID PRIMARY KEY,
    equipment_code        UUID NOT NULL,
    client_code           UUID NOT NULL,
    master_code           UUID NOT NULL,
    order_status          UUID NOT NULL,
    order_date            DATE NOT NULL CHECK (order_date > '1980-01-01'),
    order_components_code UUID
);

--changeset DDD:1.0.11
ALTER TABLE masters_list
    ADD CONSTRAINT fk_masters_list_post_code
        FOREIGN KEY (post_code) REFERENCES posts (post_code) ON DELETE CASCADE;

--changeset DDD:1.0.12
ALTER TABLE components_order
    ADD CONSTRAINT fk_components_order_component_code
        FOREIGN KEY (component_code) REFERENCES components_warehouse (components_code) ON DELETE CASCADE;

--changeset DDD:1.0.13
ALTER TABLE components_order
    ADD CONSTRAINT fk_components_order_execution_code
        FOREIGN KEY (execution_code) REFERENCES order_executions (ex_code) ON DELETE CASCADE;

--changeset DDD:1.0.14
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_equipment_code
        FOREIGN KEY (equipment_code) REFERENCES equipments (eq_code) ON DELETE CASCADE;

--changeset DDD:1.0.15
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_client_code
        FOREIGN KEY (client_code) REFERENCES clients (client_code) ON DELETE CASCADE;

--changeset DDD:1.0.16
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_master_code
        FOREIGN KEY (master_code) REFERENCES masters_list (master_code) ON DELETE CASCADE;

--changeset DDD:1.0.17
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_order_status
        FOREIGN KEY (order_status) REFERENCES orders_statuses (status_code) ON DELETE CASCADE;

--changeset DDD:1.0.18
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_order_components_code
        FOREIGN KEY (order_components_code) REFERENCES components_order (co_code) ON DELETE SET NULL;

--changeset DDD:1.0.19
CREATE UNIQUE INDEX idx_masters_list_full_name
    ON masters_list (surname, name, patronymic);

