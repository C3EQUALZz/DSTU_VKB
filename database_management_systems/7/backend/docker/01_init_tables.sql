-- Удаление существующих таблиц --
DROP TABLE IF EXISTS position_of_master CASCADE;
DROP TABLE IF EXISTS equipment CASCADE;
DROP TABLE IF EXISTS client CASCADE;
DROP TABLE IF EXISTS component_warehouse CASCADE;
DROP TABLE IF EXISTS order_fulfillment CASCADE;
DROP TABLE IF EXISTS component_order CASCADE;
DROP TABLE IF EXISTS booking CASCADE;
DROP TABLE IF EXISTS list_of_masters CASCADE;
DROP TABLE IF EXISTS status_of_booking CASCADE;
DROP DOMAIN IF EXISTS phone_number CASCADE;
DROP DOMAIN IF EXISTS serial_number CASCADE;
DROP INDEX IF EXISTS idx_list_of_masters_surname;
DROP INDEX IF EXISTS idx_list_of_masters_name;

-- Тип данных для номера телефона --
CREATE DOMAIN phone_number AS VARCHAR(12)
    CHECK (VALUE ~ '^(\+7|8)[0-9]{10}$');

-- Тип данных для серийного номера продукта --
CREATE DOMAIN serial_number AS VARCHAR(20)
    CHECK (VALUE ~ '^[A-Za-z0-9]{5,20}$');

-- Тип данных для проверки фамилии, имени и отчества --
CREATE DOMAIN human_fullname_component AS VARCHAR(30)
    CHECK (VALUE ~ '^[A-Za-zА-Яа-яёЁ-]+$');

-- Должность --
CREATE TABLE position_of_master
(
    id   INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(30) NOT NULL UNIQUE
);

-- Выполнение заказа --
CREATE TABLE order_fulfillment
(
    id                 INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    type_of_work       VARCHAR(50)    NOT NULL,
    cost               NUMERIC(10, 2) NOT NULL,
    cost_of_components NUMERIC(10, 2),
    total_cost         NUMERIC(10, 2) GENERATED ALWAYS AS (cost + COALESCE(cost_of_components, 0)) STORED,
    fulfillment_date   DATE           NOT NULL CHECK (fulfillment_date > '1980-01-01')
);

-- Статус заказа --
CREATE TABLE status_of_booking
(
    id   INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(30) NOT NULL UNIQUE
);

-- Оборудование --
CREATE TABLE equipment
(
    id            INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name          VARCHAR(50)   NOT NULL,
    serial_number serial_number NOT NULL,
    model         VARCHAR(50)   NOT NULL
);

-- Клиент --
CREATE TABLE client
(
    id         INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    surname    human_fullname_component NOT NULL,
    name       human_fullname_component NOT NULL,
    patronymic human_fullname_component NOT NULL,
    number     phone_number             NOT NULL
);

-- Склад комплектующих --
CREATE TABLE component_warehouse
(
    id            INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name          VARCHAR(30)    NOT NULL,
    amount        INTEGER        NOT NULL,
    cost_per_unit NUMERIC(10, 2) NOT NULL
);

-- Список мастеров --
CREATE TABLE list_of_masters
(
    id                 INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    position_id        INTEGER                  NOT NULL,
    surname            human_fullname_component NOT NULL,
    name               human_fullname_component NOT NULL,
    patronymic         human_fullname_component NOT NULL,
    address            VARCHAR(100)             NOT NULL,
    number             phone_number             NOT NULL,
    date_of_employment DATE                     NOT NULL CHECK (date_of_employment > '1980-01-01'),
    FOREIGN KEY (position_id) REFERENCES position_of_master (id) ON DELETE CASCADE
);

-- Заказ комплектующих --
CREATE TABLE component_order
(
    id                   INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    component_id         INTEGER NOT NULL,
    order_fulfillment_id INTEGER NOT NULL,
    FOREIGN KEY (component_id) REFERENCES component_warehouse (id) ON DELETE CASCADE,
    FOREIGN KEY (order_fulfillment_id) REFERENCES order_fulfillment (id) ON DELETE CASCADE
);

-- Заказ --
CREATE TABLE booking
(
    id                 INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    equipment_id       INTEGER NOT NULL,
    client_id          INTEGER NOT NULL,
    master_id          INTEGER NOT NULL,
    status_id          INTEGER NOT NULL,
    component_order_id INTEGER NOT NULL,
    booking_date       DATE    NOT NULL CHECK (booking_date > '1980-01-01'),
    FOREIGN KEY (equipment_id) REFERENCES equipment (id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES client (id) ON DELETE CASCADE,
    FOREIGN KEY (master_id) REFERENCES list_of_masters (id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES status_of_booking (id) ON DELETE CASCADE,
    FOREIGN KEY (component_order_id) REFERENCES component_order (id) ON DELETE CASCADE
);

CREATE INDEX idx_list_of_masters_surname ON list_of_masters (surname);
CREATE INDEX idx_list_of_masters_name ON list_of_masters (name);