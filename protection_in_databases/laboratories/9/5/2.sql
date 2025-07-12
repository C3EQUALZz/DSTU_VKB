-- Создаем таблицу с зашифрованным полем diagnosis
CREATE TABLE medical_records (
    record_id SERIAL PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    diagnosis BYTEA NOT NULL  -- Зашифрованный диагноз
);

COMMENT ON TABLE medical_records IS 'Медицинские записи с зашифрованным диагнозом';
COMMENT ON COLUMN medical_records.diagnosis IS 'Зашифрованный диагноз (требует дешифровки при выборке)';

GRANT CONNECT ON DATABASE ninth_laboratory_database_var_5 TO user2;
GRANT USAGE ON SCHEMA public TO user2;
GRANT SELECT, INSERT ON medical_records TO user2;
GRANT USAGE, SELECT ON SEQUENCE medical_records_record_id_seq TO user2;