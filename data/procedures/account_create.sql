DROP FUNCTION IF EXISTS account_create(VARCHAR, INT, DECIMAL);

CREATE FUNCTION account_create(
    p_name VARCHAR(50),
    p_default_currency_id INT,
    p_balance DECIMAL
)
RETURNS INT AS $$
DECLARE
    v_new_account_id INT;
BEGIN
    INSERT INTO account (
        name
    )
    VALUES (
        p_name
    )
    RETURNING id INTO v_new_account_id;
    INSERT INTO balance (
        account_id,
        currency_id,
        balance
    )
    VALUES (
        v_new_account_id,
        p_default_currency_id,
        p_balance
    );
    RETURN v_new_account_id;
END; $$
LANGUAGE PLPGSQL;