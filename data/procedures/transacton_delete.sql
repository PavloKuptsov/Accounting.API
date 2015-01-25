DROP FUNCTION IF EXISTS transacton_delete(INT);

CREATE FUNCTION transacton_delete(
    p_id INT
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM transaction
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;