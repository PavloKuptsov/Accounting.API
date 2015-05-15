DROP FUNCTION IF EXISTS category_create(VARCHAR, INT, INT);

CREATE FUNCTION category_create(
    p_name VARCHAR(50),
    p_parent_category_id INT,
    p_type_id INT
)
RETURNS INT AS $$
DECLARE
    v_new_category_id INT;
BEGIN
    INSERT INTO category (
        name,
        parent_category_id,
        type_id
    )
    VALUES (
        p_name,
        p_parent_category_id,
        p_type_id
    )
    RETURNING id INTO v_new_category_id;
END; $$
LANGUAGE PLPGSQL;