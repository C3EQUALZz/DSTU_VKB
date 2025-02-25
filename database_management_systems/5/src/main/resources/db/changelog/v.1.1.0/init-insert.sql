--liquibase formatted sql

--changeset DDD:249
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
--rollback DROP EXTENSION IF EXISTS "uuid-ossp"

--changeset DDD:250
INSERT INTO posts (post_code, post_name)
VALUES (uuid_generate_v4(), 'Менеджер'),
       (uuid_generate_v4(), 'Инженер'),
       (uuid_generate_v4(), 'Техник');
--rollback DELETE FROM posts;

--changeset DDD:251
INSERT INTO masters_list (master_code, post_code, surname, name, patronymic, address, phone_number, date_of_employment)
VALUES (uuid_generate_v4(), (SELECT post_code FROM posts WHERE post_name = 'Менеджер'), 'Иванов', 'Иван', 'Иванович',
        'Москва, ул. Ленина, д. 1', '+79123456789', '2020-01-15'),
       (uuid_generate_v4(), (SELECT post_code FROM posts WHERE post_name = 'Инженер'), 'Петров', 'Петр', 'Петрович',
        'Москва, ул. Пушкина, д. 2', '+79876543210', '2019-03-20');
--rollback DELETE FROM masters_list;

--changeset DDD:252
INSERT INTO orders_statuses (status_code, status_name)
VALUES (uuid_generate_v4(), 'В ожидании'),
       (uuid_generate_v4(), 'Выполнен'),
       (uuid_generate_v4(), 'Отменен');
--rollback DELETE FROM order_statuses;

--changeset DDD:253
INSERT INTO equipments (eq_code, eq_name, eq_serial_number, model)
VALUES (uuid_generate_v4(), 'Станок', 'SN123456', 'Model A'),
       (uuid_generate_v4(), 'Дрель', 'SN654321', 'Model B');
--rollback DELETE FROM components_equipments;

--changeset DDD:254
INSERT INTO clients (client_code, surname, name, patronymic, phone_number, email, password)
VALUES (uuid_generate_v4(), 'Сидоров', 'Сидор', 'Сидорович', '+71112223333', 'ggg@gmail.ru', '{noop}123'),
       (uuid_generate_v4(), 'Кузнецов', 'Алексей', 'Алексеевич', '+78444555666', 'gggf@gmail.ru', '{noop}123');
--rollback DELETE FROM clients;

--changeset DDD:255
INSERT INTO components_warehouse (components_code, component_name, components_amount, unit_cost)
VALUES (uuid_generate_v4(), 'Резистор', 100, 0.10),
       (uuid_generate_v4(), 'Конденсатор', 50, 0.20),
       (uuid_generate_v4(), 'Транзистор', 200, 0.15);
--rollback DELETE FROM components_warehouse;

--changeset DDD:256
INSERT INTO order_executions (ex_code, type_of_work, ex_cost, components_cost, ex_date)
VALUES (uuid_generate_v4(), 'Сборка', 1000.00, 50.00, '2023-01-10'),
       (uuid_generate_v4(), 'Ремонт', 500.00, 20.00, '2023-02-15');
--rollback DELETE FROM order_executions;

--changeset DDD:257
INSERT INTO components_order (co_code, component_code, execution_code)
VALUES (uuid_generate_v4(), (SELECT components_code FROM components_warehouse WHERE component_name = 'Резистор'),
        (SELECT ex_code FROM order_executions WHERE type_of_work = 'Сборка')),
       (uuid_generate_v4(), (SELECT components_code FROM components_warehouse WHERE component_name = 'Конденсатор'),
        (SELECT ex_code FROM order_executions WHERE type_of_work = 'Ремонт'));
--rollback DELETE FROM components_order;

--changeset DDD:258
INSERT INTO orders (order_code, equipment_code, client_code, master_code, order_status, order_date,
                    order_components_code)
VALUES (uuid_generate_v4(), (SELECT eq_code FROM equipments WHERE eq_name = 'Станок'),
        (SELECT client_code FROM clients WHERE surname = 'Сидоров'),
        (SELECT master_code FROM masters_list WHERE surname = 'Иванов'),
        (SELECT status_code FROM orders_statuses WHERE status_name = 'В ожидании'), '2023-03-01',
        (SELECT co_code FROM components_order LIMIT 1));
--rollback DELETE FROM orders;