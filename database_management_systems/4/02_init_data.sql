-- Заполнение таблицы "position_of_master" (должности)
INSERT INTO position_of_master (name)
VALUES ('Электрик'),
       ('Сантехник'),
       ('Механик'),
       ('Техник по ремонту');

-- Заполнение таблицы "list_of_masters" (список мастеров)
INSERT INTO list_of_masters (position_id, surname, name, patronymic, address, number, date_of_employment)
VALUES (1, 'Иванов', 'Иван', 'Иванович', 'г. Москва, ул. Ленина, д. 1', '+79991234567', '2010-05-12'),
       (2, 'Петров', 'Петр', 'Петрович', 'г. Санкт-Петербург, ул. Невская, д. 10', '+79997654321', '2012-03-08'),
       (3, 'Сидоров', 'Семен', 'Семенович', 'г. Казань, ул. Кремлевская, д. 5', '+79991112233', '2015-07-20'),
       (4, 'Кузнецов', 'Николай', 'Александрович', 'г. Екатеринбург, ул. Центральная, д. 3', '+79998887766',
        '2020-10-15');

-- Заполнение таблицы "equipment" (оборудование)
INSERT INTO equipment (name, serial_number, model)
VALUES ('Ноутбук', 'SN12345ABCDE', 'Dell Inspiron 15'),
       ('Смартфон', 'SN54321ZYXWV', 'Samsung Galaxy S21'),
       ('Принтер', 'SN67890QWERT', 'HP LaserJet Pro'),
       ('Телевизор', 'SN09876ASDFG', 'LG OLED55CX');

-- Заполнение таблицы "client" (клиенты)
INSERT INTO client (surname, name, patronymic, number)
VALUES ('Смирнов', 'Алексей', 'Иванович', '+79991231234'),
       ('Ковалев', 'Дмитрий', 'Сергеевич', '+79991114455'),
       ('Никитин', 'Виктор', 'Алексеевич', '+79992221122'),
       ('Федоров', 'Сергей', 'Олегович', '+79993334455');

-- Заполнение таблицы "component_warehouse" (склад комплектующих)
INSERT INTO component_warehouse (name, amount, cost_per_unit)
VALUES ('Кабель HDMI', 100, 350.00),
       ('Аккумулятор для ноутбука', 50, 4500.00),
       ('Тонер для принтера', 30, 1200.00),
       ('Материнская плата', 10, 9500.00);

-- Заполнение таблицы "order_fulfillment" (выполнение заказов)
INSERT INTO order_fulfillment (type_of_work, cost, cost_of_components, fulfillment_date)
VALUES ('Замена экрана смартфона', 2000.00, 1500.00, '2023-08-01'),
       ('Установка программного обеспечения', 1000.00, NULL, '2023-08-10'),
       ('Ремонт принтера', 2500.00, 800.00, '2023-08-15'),
       ('Настройка ТВ', 500.00, NULL, '2023-08-20');

-- Заполнение таблицы "status_of_booking" (статусы заказа)
INSERT INTO status_of_booking (name)
VALUES ('В обработке'),
       ('Выполняется'),
       ('Завершено'),
       ('Отменено');

-- Заполнение таблицы "component_order" (заказ комплектующих)
INSERT INTO component_order (component_id, order_fulfillment_id)
VALUES (1, 1),
       (2, 2),
       (3, 3),
       (4, 4);

-- Заполнение таблицы "booking" (заказы)
INSERT INTO booking (equipment_id, client_id, master_id, status_id, component_order_id, booking_date)
VALUES (1, 1, 1, 1, 1, '2023-08-01'),
       (2, 2, 2, 2, 2, '2023-08-05'),
       (3, 3, 3, 3, 3, '2023-08-10'),
       (4, 4, 4, 4, 4, '2023-08-15');
