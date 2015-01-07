DROP TABLE IF EXISTS account;

CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    owner_id INT,
    default_currency_id INT
);

INSERT INTO account ( id, name, owner_id, default_currency_id ) VALUES
    (1, 'Cash', NULL, 1);

GRANT ALL ON account TO accounting;