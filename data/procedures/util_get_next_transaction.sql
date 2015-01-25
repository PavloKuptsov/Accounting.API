DROP FUNCTION IF EXISTS util_get_next_transaction(INT, INT);

CREATE FUNCTION util_get_next_transaction(
    p_id INT,
    p_balance_id INT
)
RETURNS INT AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT a.transaction_id INTO v_id
    FROM (SELECT * FROM transaction_by_date_id WHERE balance_id = p_balance_id) a
    WHERE id = (SELECT id
        FROM transaction_by_date_id
        WHERE transaction_id = p_id
        )+1;
    RETURN v_id;
END; $$
LANGUAGE PLPGSQL;