DROP FUNCTION IF EXISTS transaction_create(INT, DECIMAL, DECIMAL, INT, INT, INT, VARCHAR(255), DATE, DECIMAL);

CREATE FUNCTION transaction_create(
    p_type_id INT,
    p_amount DECIMAL,
    p_previous_balance DECIMAL,
    p_balance_id INT,
    p_target_balance_id INT,
    p_category_id INT,
    p_comment VARCHAR(255),
    p_date DATE,
    p_rate DECIMAL
)
RETURNS INT AS $$
DECLARE
    v_new_transaction_id INT;
    v_previous_balance DECIMAL;
BEGIN
    INSERT INTO transaction (
        type_id,
        amount,
        target_balance_id,
        previous_balance,
        balance_id,
        category_id,
        comment,
        date,
        exchange_rate
    )
    VALUES (
        p_type_id,
        p_amount,
        p_target_balance_id,
        p_previous_balance,
        p_balance_id,
        p_category_id,
        p_comment,
        p_date,
        p_rate
    )
    RETURNING id INTO v_new_transaction_id;

    PERFORM balance_transaction_change(p_type_id, p_amount, p_balance_id, p_target_balance_id, p_previous_balance, p_rate);

    RETURN v_new_transaction_id;
END; $$
LANGUAGE PLPGSQL;