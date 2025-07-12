USE master;
GO

-- 1. Главный ключ (если еще не создан)
IF NOT EXISTS (SELECT * FROM sys.symmetric_keys WHERE name = '##MS_DatabaseMasterKey##')
BEGIN
    CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongMasterKey!123';
    PRINT 'Master Key created';
END
ELSE
    PRINT 'Master Key already exists';
GO

-- 2. Сертификат
CREATE CERTIFICATE MyTDECert
   WITH SUBJECT = 'TDE Certificate for TestDB';
GO

-- 3. Создаем тестовую БД
IF DB_ID('TestDB') IS NULL
BEGIN
    CREATE DATABASE TestDB;
    PRINT 'Database TestDB created';
END
ELSE
    PRINT 'Database TestDB already exists';
GO

USE TestDB;
GO

-- 4. Ключ шифрования БД
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE MyTDECert;
GO

-- 5. Включаем TDE
ALTER DATABASE TestDB SET ENCRYPTION ON;
GO