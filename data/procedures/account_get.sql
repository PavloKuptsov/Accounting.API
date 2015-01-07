DROP FUNCTION IF EXISTS account_get(p_id INT);

CREATE FUNCTION account_get(
    p_id INT
)
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
    FROM account a
    WHERE a.id = p_id;
END; $$
LANGUAGE PLPGSQL;