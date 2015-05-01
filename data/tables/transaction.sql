DROP TABLE IF EXISTS transaction CASCADE;

CREATE TABLE transaction (
    id SERIAL PRIMARY KEY,
    type_id INT,
    amount DECIMAL,
    balance_id INT,
    target_balance_id INT,
    previous_balance DECIMAL,
    category_id INT,
    comment VARCHAR(255),
    date DATE,
    exchange_rate DECIMAL DEFAULT 1
);

CREATE INDEX idx_id_transaction
ON transaction (id);

CREATE INDEX idx_date_transaction
ON transaction (date);