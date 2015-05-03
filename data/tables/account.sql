DROP TABLE IF EXISTS account;

CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    type_id INT,
    name VARCHAR(100),
    owner_id INT
);

CREATE INDEX idx_id_account
ON account (id);

INSERT INTO account ( id, type_id, name, owner_id ) VALUES
    (1, NULL, 'Cash', NULL),
    (2, NULL, 'Credit Card', NULL);