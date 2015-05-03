DROP FUNCTION IF EXISTS account_change(INT, VARCHAR(50));

CREATE FUNCTION account_change(
    p_id INT,
    p_name VARCHAR(50)
)
RETURNS VOID AS $$
BEGIN
    UPDATE account
    SET
        name = p_name
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;