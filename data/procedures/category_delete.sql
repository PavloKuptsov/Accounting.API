DROP FUNCTION IF EXISTS category_delete(INT, INT);

CREATE FUNCTION category_delete(
    p_id INT,
    p_new_category_id INT
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM category
    WHERE id = p_id;

    UPDATE transaction SET
        category_id = p_new_category_id
    WHERE category_id = p_id;
END; $$
LANGUAGE PLPGSQL;