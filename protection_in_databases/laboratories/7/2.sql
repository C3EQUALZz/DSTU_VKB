USE TestDB;
GO

-- 1. Создаем таблицу для хранения зашифрованных данных
CREATE TABLE EncryptedSecrets (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    SecretName NVARCHAR(100) NOT NULL,
    EncryptedData VARBINARY(MAX) NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);
GO

-- 2. Процедура для вставки зашифрованных данных
CREATE PROCEDURE InsertEncryptedSecret
    @SecretName NVARCHAR(100),
    @PlainText NVARCHAR(MAX)
AS
BEGIN
    -- Шифруем данные с помощью парольной фразы
    DECLARE @Encrypted VARBINARY(MAX);
    SET @Encrypted = ENCRYPTBYPASSPHRASE('MySuperSecretPassphrase!123', @PlainText);

    -- Вставляем зашифрованные данные в таблицу
    INSERT INTO EncryptedSecrets (SecretName, EncryptedData)
    VALUES (@SecretName, @Encrypted);

    PRINT 'Encrypted data inserted successfully.';
END;
GO

-- 3. Процедура для получения зашифрованных данных (без дешифровки)
CREATE PROCEDURE GetEncryptedSecrets
AS
BEGIN
    -- Возвращаем данные в зашифрованном виде (как требует задание)
    SELECT
        ID,
        SecretName,
        EncryptedData AS EncryptedContent, -- Зашифрованные данные
        CreatedAt
    FROM EncryptedSecrets;
END;
GO

-- 4. Процедура для дешифровки данных (дополнительно, для проверки)
CREATE PROCEDURE DecryptSecret
    @SecretID INT
AS
BEGIN
    SELECT
        ID,
        SecretName,
        CONVERT(NVARCHAR(MAX),
            DECRYPTBYPASSPHRASE('MySuperSecretPassphrase!123', EncryptedData))
            AS DecryptedContent,
        CreatedAt
    FROM EncryptedSecrets
    WHERE ID = @SecretID;
END;
GO


