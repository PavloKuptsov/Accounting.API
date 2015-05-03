DROP FUNCTION IF EXISTS transaction_delete(INT);

CREATE FUNCTION transaction_delete(
    p_id INT
)
RETURNS BOOL AS $$
    DECLARE
        v_type_id INT;
        v_balance_id INT;
        v_amount DECIMAL;
BEGIN
    SELECT type_id, balance_id, amount INTO v_type_id, v_balance_id, v_amount
    FROM transaction
    WHERE id = p_id;
    PERFORM balance_transaction_reverse_change(v_type_id, v_amount, v_balance_id);

    SELECT type_id, balance_id, amount INTO v_type_id, v_balance_id, v_amount
    FROM transaction
    WHERE child_to = p_id;
    PERFORM balance_transaction_reverse_change(v_type_id, v_amount, v_balance_id);

    DELETE FROM transaction
    WHERE id = p_id;

    DELETE FROM transaction
    WHERE child_to = p_id;
    RETURN TRUE;
END; $$
LANGUAGE PLPGSQL;