DROP FUNCTION IF EXISTS balance_create(INT, INT, DECIMAL);

CREATE FUNCTION balance_create(
    p_account_id INT,
    p_currency_id INT,
    p_balance DECIMAL
)
RETURNS INT AS $$
DECLARE
    v_new_balance_id INT;
BEGIN
    INSERT INTO balance (
        account_id,
        currency_id,
        balance
    )
    VALUES (
        p_account_id,
        p_currency_id,
        p_balance
    )
    RETURNING id INTO v_new_balance_id;
    RETURN v_new_balance_id;
END; $$
LANGUAGE PLPGSQL;