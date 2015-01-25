DROP FUNCTION IF EXISTS util_get_last_transaction_to_date(INT, DATE);

CREATE FUNCTION util_get_last_transaction_to_date(
    p_balance_id INT,
    p_date DATE
)
RETURNS INT AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT max(a.transaction_id) INTO v_id
    FROM (SELECT * FROM transaction_by_date_id WHERE balance_id = p_balance_id AND date <= p_date) a;
    RETURN v_id;
END; $$
LANGUAGE PLPGSQL;