DROP FUNCTION IF EXISTS balance_change(INT, DECIMAL);

CREATE FUNCTION balance_change(
    p_id INT,
    p_balance DECIMAL
)
RETURNS VOID AS $$
BEGIN
    UPDATE balance
    SET
        balance = p_balance
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;