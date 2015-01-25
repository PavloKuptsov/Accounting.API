DROP VIEW IF EXISTS transaction_by_date_id;

CREATE VIEW transaction_by_date_id AS
SELECT
    row_number() OVER(ORDER BY balance_id ASC, date ASC, id ASC) AS id,
    date,
    id AS transaction_id,
    balance_id
FROM transaction
ORDER BY balance_id ASC, date ASC, id ASC;