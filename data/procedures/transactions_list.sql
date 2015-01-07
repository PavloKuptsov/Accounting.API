DROP FUNCTION IF EXISTS transactions_list();

CREATE FUNCTION transactions_list()
RETURNS TABLE (
    id INT,
    type_id INT,
    amount DECIMAL,
    previous_balance DECIMAL,
    balance_id INT,
    target_balance_id INT,
    category_id INT,
    comment VARCHAR(255),
    date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id,
        t.type_id,
        t.amount,
        t.previous_balance,
        t.balance_id,
        t.target_balance_id,
        t.category_id,
        t.comment,
        t.date
    FROM transaction t
    ORDER BY t.date;
END;
$$
LANGUAGE PLPGSQL;