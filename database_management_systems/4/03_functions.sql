/**
  Функция для получения данных о клиенте по его ID.
  Пример использования:
  SELECT * FROM get_client(1);
*/
CREATE OR REPLACE FUNCTION get_client(
    p_id INTEGER
)
    RETURNS TABLE
            (
                id         INTEGER,
                surname    human_fullname_component,
                name       human_fullname_component,
                patronymic human_fullname_component,
                number     phone_number
            )
    LANGUAGE plpgsql
AS
'
    BEGIN
        RETURN QUERY
            SELECT client.id,
                   client.surname,
                   client.name,
                   client.patronymic,
                   client.number
            FROM client
            WHERE client.id = p_id;
    END;
';



/**
  Функция для добавления нового клиента.
  Пример использования:
  SELECT add_client('Иванов', 'Иван', 'Иванович', '+79991234567');
*/
CREATE OR REPLACE FUNCTION add_client(
    p_surname human_fullname_component,
    p_name human_fullname_component,
    p_patronymic human_fullname_component,
    p_number phone_number
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        INSERT INTO client (surname, name, patronymic, number)
        VALUES (p_surname, p_name, p_patronymic, p_number);
    END;
';

/**
  Функция для обновления данных клиента.
  Пример использования:
  SELECT update_client(1, 'Петров', 'Петр', NULL, '+79990001122');
*/
CREATE OR REPLACE FUNCTION update_client(
    p_id INTEGER,
    p_new_surname human_fullname_component DEFAULT NULL,
    p_new_name human_fullname_component DEFAULT NULL,
    p_new_patronymic human_fullname_component DEFAULT NULL,
    p_new_number phone_number DEFAULT NULL
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        UPDATE client
        SET surname    = COALESCE(p_new_surname, surname),
            name       = COALESCE(p_new_name, name),
            patronymic = COALESCE(p_new_patronymic, patronymic),
            number     = COALESCE(p_new_number, number)
        WHERE client.id = p_id;
    END;
';


/**
  Функция для удаления клиента по его ID.
  Пример использования:
  SELECT delete_client(1);
*/
CREATE OR REPLACE FUNCTION delete_client(
    p_id INTEGER
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        DELETE
        FROM client
        WHERE client.id = p_id;
    END;
';

/**
  Функция для получения данных о компоненте по его ID.
  Пример использования:
  SELECT * FROM get_component(1);
*/
CREATE OR REPLACE FUNCTION get_component(
    p_id INTEGER
)
    RETURNS TABLE
            (
                id            INTEGER,
                name          VARCHAR(30),
                amount        INTEGER,
                cost_per_unit NUMERIC(10, 2)
            )
    LANGUAGE plpgsql
AS
'
    BEGIN
        RETURN QUERY
            SELECT component_warehouse.id,
                   component_warehouse.name,
                   component_warehouse.amount,
                   component_warehouse.cost_per_unit
            FROM component_warehouse
            WHERE component_warehouse.id = p_id;
    END;
';

/**
  Функция для добавления нового компонента на склад.
  Пример использования:
  SELECT add_component('Резистор', 100, 1.50);
*/
CREATE OR REPLACE FUNCTION add_component(
    p_name VARCHAR(30),
    p_amount INTEGER,
    p_cost_per_unit NUMERIC(10, 2)
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        INSERT INTO component_warehouse (name, amount, cost_per_unit)
        VALUES (p_name, p_amount, p_cost_per_unit);
    END;
';

/**
  Функция для обновления данных о компоненте.
  Пример использования:
  SELECT update_component(1, 'Конденсатор', 200, 0.75);
*/
CREATE OR REPLACE FUNCTION update_component(
    p_id INTEGER,
    p_new_name VARCHAR(30) DEFAULT NULL,
    p_new_amount INTEGER DEFAULT NULL,
    p_new_cost_per_unit NUMERIC(10, 2) DEFAULT NULL
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        UPDATE component_warehouse
        SET name          = COALESCE(p_new_name, name),
            amount        = COALESCE(p_new_amount, amount),
            cost_per_unit = COALESCE(p_new_cost_per_unit, cost_per_unit)
        WHERE component_warehouse.id = p_id;
    END;
';


/**
  Функция для удаления компонента по его ID.
  Пример использования:
  SELECT delete_component(1);
*/
CREATE OR REPLACE FUNCTION delete_component(
    p_id INTEGER
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        DELETE
        FROM component_warehouse
        WHERE component_warehouse.id = p_id;
    END;
';


/**
  Функция для добавления нового мастера в таблицу list_of_masters
  Пример использования:
  SELECT add_master(1, 'Иванов', 'Иван', 'Иванович', 'г. Москва, ул. Ленина, д. 1', '+79991234567', '2010-05-12');
 */
CREATE OR REPLACE FUNCTION add_master(
    p_position_id INTEGER,
    p_surname VARCHAR(30),
    p_name VARCHAR(30),
    p_patronymic VARCHAR(30),
    p_address VARCHAR(100),
    p_number phone_number,
    p_date_of_employment DATE
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        INSERT INTO list_of_masters (position_id, surname, name, patronymic, address, number, date_of_employment)
        VALUES (p_position_id, p_surname, p_name, p_patronymic, p_address, p_number, p_date_of_employment);
    END;
';

/**
  Функция для изменения данных о мастерах.
  Здесь мы, например, обновляем информацию о адресе.
  Примеры использования:
  1. SELECT update_master(1, p_address => 'г. Санкт-Петербург, ул. Невская, д. 10');
  2. SELECT update_master(1, p_name => 'Алексей', p_date_of_employment => '2020-01-15');
  3. SELECT update_master(
    1,
    p_position_id => 2,
    p_surname => 'Кузнецов',
    p_name => 'Николай',
    p_patronymic => 'Александрович',
    p_address => 'г. Екатеринбург, ул. Центральная, д. 3',
    p_number => '+79998887766',
    p_date_of_employment => '2020-10-15'
);
 */
CREATE OR REPLACE FUNCTION update_master(
    p_master_id INTEGER,
    p_position_id INTEGER DEFAULT NULL,
    p_surname VARCHAR(30) DEFAULT NULL,
    p_name VARCHAR(30) DEFAULT NULL,
    p_patronymic VARCHAR(30) DEFAULT NULL,
    p_address VARCHAR(100) DEFAULT NULL,
    p_number phone_number DEFAULT NULL,
    p_date_of_employment DATE DEFAULT NULL
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        UPDATE list_of_masters
        SET position_id        = COALESCE(p_position_id, position_id),
            surname            = COALESCE(p_surname, surname),
            name               = COALESCE(p_name, name),
            patronymic         = COALESCE(p_patronymic, patronymic),
            address            = COALESCE(p_address, address),
            number             = COALESCE(p_number, number),
            date_of_employment = COALESCE(p_date_of_employment, date_of_employment)
        WHERE list_of_masters.id = p_master_id;
    END;
';

/**
  Функция для удаления мастера из таблицы list_of_masters по id.
  Пример использования: SELECT delete_master(1);
 */
CREATE OR REPLACE FUNCTION delete_master(
    p_master_id INTEGER
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        DELETE
        FROM list_of_masters
        WHERE list_of_masters.id = p_master_id;
    END;
';

/**
  Функция для добавления позиции мастера.
  Пример использования: SELECT add_position('Инженер');
 */
CREATE OR REPLACE FUNCTION add_position(
    p_name VARCHAR(30)
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        INSERT INTO position_of_master (name)
        VALUES (p_name);
    END;
';

/**
  Функция для обновления позиции мастера.
  Пример использования SELECT update_position(1, 'Ученик');
 */
CREATE OR REPLACE FUNCTION update_position(
    p_id INTEGER,
    p_name VARCHAR(30) DEFAULT NULL
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        UPDATE position_of_master
        SET name = COALESCE(p_name, name)
        WHERE position_of_master.id = p_id;
    EXCEPTION
        WHEN unique_violation THEN
            RAISE NOTICE ''Позиция с таким именем уже существует: %'', p_name;
    END;
';


/**
  Функция для удаления позиции мастера.
  Пример использования: SELECT delete_position('1')
 */
CREATE OR REPLACE FUNCTION delete_position(
    p_id INTEGER
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        DELETE
        FROM position_of_master
        WHERE id = p_id;

        IF NOT FOUND THEN
            RAISE NOTICE ''Статус с ID % не найден.'', p_id;
        END IF;
    END;
';

/**
  Функция для добавления нового статуса заказа.
  Примеры использования:
  1. SELECT add_booking_status('В обработке');
  2. SELECT add_booking_status('Завершён');
 */
CREATE OR REPLACE FUNCTION add_booking_status(
    p_status_name VARCHAR(30)
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        INSERT INTO status_of_booking (name)
        VALUES (p_status_name);
    EXCEPTION
        WHEN unique_violation THEN
            RAISE NOTICE ''Статус с таким именем уже существует: %'', p_status_name;
    END;
';

/**
   Функция для обновления статуса заказа.
   Примеры использования:
   1. SELECT update_booking_status(1, 'На рассмотрении');
   2. SELECT update_booking_status(2, 'Отменён');
*/
CREATE OR REPLACE FUNCTION update_booking_status(
    p_status_id INTEGER,
    p_new_name VARCHAR(30)
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        UPDATE status_of_booking
        SET name = p_new_name
        WHERE id = p_status_id;

        IF NOT FOUND THEN
            RAISE NOTICE ''Статус с ID % не найден.'', p_status_id;
        END IF;
    EXCEPTION
        WHEN unique_violation THEN
            RAISE NOTICE ''Статус с таким именем уже существует: %'', p_new_name;
    END;
';

/**
  Функция для удаления статуса покупки.
  Пример использования: SELECT delete_booking_status(3);
 */
CREATE OR REPLACE FUNCTION delete_booking_status(
    p_status_id INTEGER
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        DELETE
        FROM status_of_booking
        WHERE status_of_booking.id = p_status_id;

        IF NOT FOUND THEN
            RAISE NOTICE ''Статус с ID % не найден.'', p_status_id;
        END IF;
    END;
';


