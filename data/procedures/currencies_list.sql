DROP FUNCTION IF EXISTS currencies_list();

CREATE FUNCTION currencies_list()
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    short_name VARCHAR(3)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.short_name
    FROM currency c;
END; $$
LANGUAGE PLPGSQL;