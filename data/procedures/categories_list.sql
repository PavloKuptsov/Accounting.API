DROP FUNCTION IF EXISTS categories_list();

CREATE FUNCTION categories_list()
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    parent_category_id INT,
    type_id INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.parent_category_id,
        c.type_id
    FROM category c;
END;
$$
LANGUAGE PLPGSQL;