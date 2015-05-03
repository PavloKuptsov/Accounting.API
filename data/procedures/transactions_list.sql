DROP FUNCTION IF EXISTS transactions_list();

CREATE FUNCTION transactions_list()
RETURNS TABLE (
    id INT,
    type_id INT,
    amount DECIMAL,
    balance_id INT,
    category_id INT,
    comment VARCHAR(255),
    date DATE,
    target_balance_id INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id,
        t.type_id,
        t.amount,
        t.balance_id,
        t.category_id,
        t.comment,
        t.date,
        t1.balance_id AS target_balance_id
    FROM transaction t
    LEFT JOIN transaction AS t1 ON t.id = t1.child_to
    WHERE t.type_id != 4
    ORDER BY t.date;
END;
$$
LANGUAGE PLPGSQL;