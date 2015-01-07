DROP FUNCTION IF EXISTS currencies_list();

CREATE FUNCTION currencies_list()
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    short_name VARCHAR(3),
    exchange_rate DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.short_name,
        c.exchange_rate
    FROM currency c;
END; $$
LANGUAGE PLPGSQL;