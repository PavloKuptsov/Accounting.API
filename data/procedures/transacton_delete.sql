DROP FUNCTION IF EXISTS transaction_delete(INT);

CREATE FUNCTION transaction_delete(
    p_id INT
)
RETURNS BOOL AS $$
BEGIN
    DELETE FROM transaction
    WHERE id = p_id;
    RETURN TRUE;
END; $$
LANGUAGE PLPGSQL;