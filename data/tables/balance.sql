DROP TABLE IF EXISTS balance;

CREATE TABLE balance (
    id SERIAL PRIMARY KEY,
    account_id INT,
    currency_id INT,
    balance DECIMAL
);

INSERT INTO balance ( id, account_id, currency_id, balance ) VALUES
    (1, 1, 1, 0),
    (2, 1, 2, 500);

GRANT ALL ON balance TO accounting;