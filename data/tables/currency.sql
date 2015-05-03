DROP TABLE IF EXISTS currency;

CREATE TABLE currency (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    short_name VARCHAR(3)
);

INSERT INTO currency ( id, name, short_name ) VALUES
    (1, 'Ukrainian Hryvna', 'UAH'),
    (2, 'US Dollar', 'USD');
--    (3, 'Euro', 'EUR');