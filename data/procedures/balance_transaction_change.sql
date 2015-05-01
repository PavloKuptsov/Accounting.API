DROP FUNCTION IF EXISTS balance_transaction_change(INT, DECIMAL, INT, INT, DECIMAL, DECIMAL);

CREATE FUNCTION balance_transaction_change(
    p_type_id INT,
    p_amount DECIMAL,
    p_balance_id INT,
    p_target_balance_id INT,
    p_previous_balance DECIMAL,
    p_rate DECIMAL
)
RETURNS void AS $$
    DECLARE v_tagret_previous_balance DECIMAL;
BEGIN
    IF p_type_id = 1 THEN --spending
        PERFORM balance_change(p_balance_id, p_previous_balance - p_amount);
    ELSIF p_type_id = 2 THEN -- income
        PERFORM balance_change(p_balance_id, p_previous_balance + p_amount);
    ELSE -- transfer
        SELECT balance INTO v_tagret_previous_balance
            FROM balance
            WHERE id = p_target_balance_id;
        PERFORM balance_change(p_balance_id, p_previous_balance - p_amount);
        PERFORM balance_change(p_target_balance_id, v_tagret_previous_balance + p_amount*p_rate);
    END IF;
END; $$
LANGUAGE PLPGSQL;