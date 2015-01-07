DROP FUNCTION IF EXISTS account_change(INT, VARCHAR(50), INT);

CREATE FUNCTION account_change(
    p_id INT,
    p_name VARCHAR(50),
    p_default_currency_id INT
)
RETURNS VOID AS $$
BEGIN
    UPDATE account
    SET
        name = p_name,
        default_currency_id = p_default_currency_id
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;