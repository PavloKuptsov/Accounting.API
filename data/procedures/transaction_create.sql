DROP FUNCTION IF EXISTS transaction_create(INT, DECIMAL, INT, INT, INT, VARCHAR(255), DATE, DECIMAL);

CREATE FUNCTION transaction_create(
    p_type_id INT,
    p_amount DECIMAL,
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
BEGIN
    INSERT INTO transaction (
        type_id,
        amount,
        balance_id,
        category_id,
        comment,
        date,
        exchange_rate,
        child_to
    )
    VALUES (
        p_type_id,
        p_amount,
        p_balance_id,
        p_category_id,
        p_comment,
        p_date,
        p_rate,
        NULL
    )
    RETURNING id INTO v_new_transaction_id;
    PERFORM balance_transaction_change(p_type_id, p_amount, p_balance_id);

    IF (p_type_id = 3)
    THEN
        INSERT INTO transaction (
            type_id,
            amount,
            balance_id,
            category_id,
            comment,
            date,
            exchange_rate,
            child_to
        )
        VALUES (
            4,
            p_amount * p_rate,
            p_target_balance_id,
            NULL,
            NULL,
            p_date,
            1,
            v_new_transaction_id
        )
        RETURNING id INTO v_new_transaction_id;
        PERFORM balance_transaction_change(4, p_amount * p_rate, p_target_balance_id);
    END IF;

    RETURN v_new_transaction_id;
END; $$
LANGUAGE PLPGSQL;