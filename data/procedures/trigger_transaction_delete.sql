DROP FUNCTION IF EXISTS trigger_transaction_delete() CASCADE;

CREATE FUNCTION trigger_transaction_delete()
RETURNS trigger AS $$
BEGIN
    UPDATE transaction
    SET previous_balance = OLD.previous_balance
    WHERE id = util_get_next_transaction(OLD.id, OLD.balance_id);
    RETURN NEW;
END; $$
LANGUAGE PLPGSQL;