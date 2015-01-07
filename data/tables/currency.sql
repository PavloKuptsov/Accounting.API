DROP TABLE IF EXISTS currency;

CREATE TABLE currency (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    short_name VARCHAR(3),
    exchange_rate DECIMAL
);

INSERT INTO currency ( id, name, short_name, exchange_rate ) VALUES
    (1, 'Ukrainian Hryvna', 'UAH', 1),
    (2, 'US Dollar', 'USD', 15);

GRANT ALL ON currency TO accounting;