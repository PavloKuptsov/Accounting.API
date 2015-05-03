DROP FUNCTION IF EXISTS balance_increase(INT, DECIMAL);

CREATE FUNCTION balance_increase(
    p_id INT,
    p_amount DECIMAL
)
RETURNS VOID AS $$
    DECLARE v_balance DECIMAL;
BEGIN
    SELECT balance + p_amount INTO v_balance
    FROM balance
    WHERE id = p_id;

    UPDATE balance
    SET
        balance = v_balance
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;