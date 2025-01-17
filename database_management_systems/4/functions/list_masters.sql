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
  Пример использования:
  SELECT update_master_address(1, 'г. Санкт-Петербург, ул. Невская, д. 10');
 */
CREATE OR REPLACE FUNCTION update_master_address(
    p_master_id INTEGER,
    p_new_address VARCHAR(100)
)
    RETURNS VOID
    LANGUAGE plpgsql AS
'
    BEGIN
        UPDATE list_of_masters
        SET address = p_new_address
        WHERE id = p_master_id;
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
        WHERE id = p_master_id;
    END;
';
