DROP TABLE IF EXISTS transaction;

CREATE TABLE transaction (
    id SERIAL PRIMARY KEY,
    type_id INT,
    amount DECIMAL,
    balance_id INT,
    target_balance_id INT,
    previous_balance DECIMAL,
    category_id INT,
    comment VARCHAR(255),
    date DATE
);

GRANT ALL ON transaction TO accounting;