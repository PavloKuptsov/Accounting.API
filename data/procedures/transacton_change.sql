--TODO: actualize
DROP FUNCTION IF EXISTS transaction_change(INT, INT, DECIMAL, INT, INT, INT, VARCHAR(255), DATE, DECIMAL);

CREATE FUNCTION transaction_change(
    p_id INT,
    p_type_id INT,
    p_amount DECIMAL,
    p_balance_id INT,
    p_target_balance_id INT,
    p_category_id INT,
    p_comment VARCHAR(255),
    p_date DATE,
    p_rate DECIMAL
)
RETURNS VOID AS $$
BEGIN
    UPDATE transaction
    SET
        type_id = p_type_id,
        amount = p_amount,
        balance_id = p_balance_id,
        category_id = p_category_id,
        comment = p_comment,
        date = p_date,
        exchange_rate = p_rate
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;