DROP FUNCTION IF EXISTS accounts_list();

CREATE FUNCTION accounts_list()
RETURNS TABLE (
    id INT,
    type_id INT,
    name VARCHAR(100),
    default_currency_id INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.type_id,
        a.name,
        a.default_currency_id
    FROM account a;
END;
$$
LANGUAGE PLPGSQL;