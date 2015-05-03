DROP FUNCTION IF EXISTS balance_transaction_reverse_change(INT, DECIMAL, INT);

CREATE FUNCTION balance_transaction_reverse_change(
    p_type_id INT,
    p_amount DECIMAL,
    p_balance_id INT
)
RETURNS void AS $$
BEGIN
    IF p_type_id = 1 OR p_type_id = 3 THEN -- spending or transfer parent
        PERFORM balance_increase(p_balance_id, p_amount);
    ELSIF p_type_id = 2 OR p_type_id = 4 THEN -- income or transfer child
        PERFORM balance_decrease(p_balance_id, p_amount);
    END IF;
END; $$
LANGUAGE PLPGSQL;