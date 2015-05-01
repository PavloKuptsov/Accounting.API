DROP TABLE IF EXISTS account;

CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    type_id INT,
    name VARCHAR(100),
    owner_id INT,
    default_currency_id INT
);

CREATE INDEX idx_id_account
ON account (id);

INSERT INTO account ( id, type_id, name, owner_id, default_currency_id ) VALUES
    (1, NULL, 'Cash', NULL, 1),
    (2, NULL, 'Credit Card', NULL, 1);