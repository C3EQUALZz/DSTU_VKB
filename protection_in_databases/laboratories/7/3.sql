USE TestDB;
GO

-- a. Создаем асимметричный ключ и защищаем его парольной фразой
CREATE ASYMMETRIC KEY MyAsymKey
    WITH ALGORITHM = RSA_2048
    ENCRYPTION BY PASSWORD = 'StrongAsymKeyPassword!123';
GO

-- b. Создаем симметричный ключ и защищаем его асимметричным ключом
CREATE SYMMETRIC KEY MySymKey
    WITH ALGORITHM = AES_256
    ENCRYPTION BY ASYMMETRIC KEY MyAsymKey;
GO

OPEN SYMMETRIC KEY MySymKey
    DECRYPTION BY ASYMMETRIC KEY MyAsymKey
    WITH PASSWORD = 'StrongAsymKeyPassword!123';
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'EncryptedWithAsym')
BEGIN
    CREATE TABLE EncryptedWithAsym (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        PlainText NVARCHAR(255),
        EncryptedData VARBINARY(256),
        CreatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT 'Table EncryptedWithAsym created';
END
ELSE
    PRINT 'Table EncryptedWithAsym already exists';

-- Вставляем данные с использованием симметричного ключа
DECLARE @SecretText NVARCHAR(255) = N'Секретная информация: 123-45-67';
DECLARE @EncryptedData VARBINARY(256);

-- Шифруем данные
SET @EncryptedData = ENCRYPTBYKEY(KEY_GUID('MySymKey'), @SecretText);

INSERT INTO EncryptedWithAsym (PlainText, EncryptedData)
VALUES (@SecretText, @EncryptedData);

PRINT 'Data encrypted and inserted successfully!';
GO

