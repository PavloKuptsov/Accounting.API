DROP FUNCTION IF EXISTS balances_search(p_account_id INT);

CREATE FUNCTION balances_search(
    p_account_id INT
)
RETURNS TABLE (
    id INT,
    account_id INT,
    currency_id INT,
    balance DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        b.id,
        b.account_id,
        b.currency_id,
        b.balance
    FROM balance b
    WHERE b.account_id = p_account_id
    ORDER BY b.currency_id;
END; $$
LANGUAGE PLPGSQL;