--liquibase formatted sql
--changeset DDD:228
ALTER TABLE masters_list
    ADD CONSTRAINT chk_masters_list_phone_number
        CHECK (phone_number ~ '^(\+7|8)[0-9]{10}$');
--rollback ALTER TABLE masters_list DROP CONSTRAINT chk_masters_list_phone_number;

--changeset DDD:229
ALTER TABLE clients
    ADD CONSTRAINT chk_clients_phone_number
        CHECK (phone_number ~ '^(\+7|8)[0-9]{10}$');
--rollback ALTER TABLE clients DROP CONSTRAINT chk_clients_phone_number;

--changeset DDD:230
ALTER TABLE equipments
    ADD CONSTRAINT chk_equipments_serial_number
        CHECK (eq_serial_number ~ '^[A-Za-z0-9]{5,20}$');
--rollback ALTER TABLE equipments DROP CONSTRAINT chk_equipments_serial_number;

--changeset DDD:231
ALTER TABLE clients
    ADD CONSTRAINT chk_clients_surname
        CHECK (surname ~ '^[A-Za-zА-Яа-яёЁ-]+$');
--rollback ALTER TABLE clients DROP CONSTRAINT chk_clients_surname;

--changeset DDD:232
ALTER TABLE clients
    ADD CONSTRAINT chk_clients_name
        CHECK (name ~ '^[A-Za-zА-Яа-яёЁ-]+$');
--rollback ALTER TABLE clients DROP CONSTRAINT chk_clients_name;

--changeset DDD:233
ALTER TABLE clients
    ADD CONSTRAINT chk_clients_patronymic
        CHECK (patronymic ~ '^[A-Za-zА-Яа-яёЁ-]+$');
--rollback ALTER TABLE clients DROP CONSTRAINT chk_clients_patronymic;

--changeset DDD:234
ALTER TABLE masters_list
    ADD CONSTRAINT chk_masters_surname
        CHECK (surname ~ '^[A-Za-zА-Яа-яёЁ-]+$');
--rollback ALTER TABLE masters_list DROP CONSTRAINT chk_masters_surname;

--changeset DDD:235
ALTER TABLE masters_list
    ADD CONSTRAINT chk_masters_name
        CHECK (name ~ '^[A-Za-zА-Яа-яёЁ-]+$');
--rollback ALTER TABLE masters_list DROP CONSTRAINT chk_masters_name;

--changeset DDD:236
ALTER TABLE masters_list
    ADD CONSTRAINT chk_masters_patronymic
        CHECK (patronymic ~ '^[A-Za-zА-Яа-яёЁ-]+$');
--rollback ALTER TABLE masters_list DROP CONSTRAINT chk_masters_patronymic;
