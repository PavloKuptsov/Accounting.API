DROP TABLE IF EXISTS transaction_type;

CREATE TABLE transaction_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO transaction_type ( id, name ) VALUES
    (1, 'Spending'),
    (2, 'Income'),
    (3, 'Transfer parent'),
    (4, 'Transfer child');