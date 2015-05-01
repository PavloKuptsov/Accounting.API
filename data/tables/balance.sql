DROP TABLE IF EXISTS balance;

CREATE TABLE balance (
    id SERIAL PRIMARY KEY,
    account_id INT,
    currency_id INT,
    balance DECIMAL
);

CREATE INDEX idx_id_balance
ON balance (id);

INSERT INTO balance ( id, account_id, currency_id, balance ) VALUES
    (1, 1, 1, 2500),
    (2, 1, 2, 500),
    (3, 2, 1, 10000);