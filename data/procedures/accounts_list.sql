DROP FUNCTION IF EXISTS accounts_list();

CREATE FUNCTION accounts_list()
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
    FROM account a;
END;
$$
LANGUAGE PLPGSQL;