DROP TABLE IF EXISTS transaction CASCADE;

CREATE TABLE transaction (
    id SERIAL PRIMARY KEY,
    type_id INT,
    amount DECIMAL,
    balance_id INT,
    category_id INT,
    comment VARCHAR(255),
    date DATE,
    exchange_rate DECIMAL DEFAULT 1,
    child_to INT DEFAULT NULL
);

CREATE INDEX idx_id_transaction
ON transaction (id);

CREATE INDEX idx_date_transaction
ON transaction (date);