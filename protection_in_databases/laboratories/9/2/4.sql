INSERT INTO payment_records (account_number, amount)
VALUES
    (encrypt_account('40817810500000000001'), 1500.75),
    (encrypt_account('40817810500000000002'), 3200.50),
    (encrypt_account('40817810500000000003'), 5400.00);