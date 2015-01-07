DROP FUNCTION IF EXISTS balance_transaction_change(INT, DECIMAL, INT, INT, DECIMAL);

CREATE FUNCTION balance_transaction_change(
    p_type_id INT,
    p_amount DECIMAL,
    p_balance_id INT,
    p_target_balance_id INT,
    p_previous_balance DECIMAL
)
RETURNS void AS $$
BEGIN
    IF p_type_id = 1 THEN
        PERFORM balance_change(p_balance_id, p_previous_balance - p_amount);
    ELSIF p_type_id = 2 THEN
        PERFORM balance_change(p_balance_id, p_previous_balance + p_amount);
    ELSE
        PERFORM balance_change(p_balance_id, p_previous_balance - p_amount);
        PERFORM balance_change(p_target_balance_id, p_previous_balance + p_amount);
    END IF;
END; $$
LANGUAGE PLPGSQL;