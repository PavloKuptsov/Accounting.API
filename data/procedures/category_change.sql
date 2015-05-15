DROP FUNCTION IF EXISTS category_change(INT, VARCHAR(50), INT, INT);

CREATE FUNCTION category_change(
    p_id INT,
    p_name VARCHAR(50),
    p_parent_category_id INT,
    p_type_id INT
)
RETURNS VOID AS $$
BEGIN
    UPDATE category
    SET
        name = p_name,
        parent_category_id = p_parent_category_id,
        type_id = p_type_id
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;