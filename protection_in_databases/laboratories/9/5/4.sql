-- Вставляем тестовые данные
INSERT INTO medical_records (patient_name, diagnosis)
VALUES
    ('Иван Иванов', encrypt_diagnosis('Гипертония II степени')),
    ('Мария Петрова', encrypt_diagnosis('Сахарный диабет 2 типа')),
    ('Алексей Сидоров', encrypt_diagnosis('Остеохондроз шейного отдела'));