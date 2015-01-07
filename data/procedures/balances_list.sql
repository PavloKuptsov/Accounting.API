DROP FUNCTION IF EXISTS balances_list();

CREATE FUNCTION balances_list()
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
    FROM balance b;
END; $$
LANGUAGE PLPGSQL;