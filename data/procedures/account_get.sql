DROP FUNCTION IF EXISTS account_get(p_id INT);

CREATE FUNCTION account_get(
    p_id INT
)
RETURNS TABLE (
    id INT,
    type_id INT,
    name VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.type_id,
        a.name
    FROM account a
    WHERE a.id = p_id;
END; $$
LANGUAGE PLPGSQL;