DROP FUNCTION IF EXISTS balance_get_last_by_date(DATE, INT);

CREATE FUNCTION balance_get_last_by_date(
    p_date DATE,
    p_balance_id INT
)
RETURNS DECIMAL AS $$
DECLARE
    v_balance DECIMAL;
BEGIN
    SELECT INTO v_balance
        CASE t.type_id
            WHEN 2 THEN
                t.previous_balance + t.amount
            ELSE
                t.previous_balance - t.amount
        END
    FROM transaction t
    WHERE t.id = (SELECT MAX(id) FROM transaction WHERE date <= p_date) AND t.balance_id = p_balance_id;
    RETURN v_balance;
END; $$
LANGUAGE PLPGSQL;