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
    END;
'