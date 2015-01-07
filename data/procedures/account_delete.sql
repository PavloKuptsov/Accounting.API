DROP FUNCTION IF EXISTS account_delete(INT);

CREATE FUNCTION account_delete(
    p_id INT
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM account
    WHERE id = p_id;

    DELETE FROM transaction
    WHERE balance_id IN (
        SELECT id
        FROM balance
        WHERE account_id = p_id);

    DELETE FROM balance
    WHERE account_id = p_id;
END; $$
LANGUAGE PLPGSQL;