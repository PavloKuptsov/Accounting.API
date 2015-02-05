DROP FUNCTION IF EXISTS trigger_transaction_delete() CASCADE;

CREATE FUNCTION trigger_transaction_delete()
RETURNS trigger AS $$
DECLARE
    v_transaction_amount_id DECIMAL;
BEGIN
    IF NOT (SELECT * FROM util_is_last_transaction(OLD.id, OLD.balance_id))
    THEN
        UPDATE transaction
        SET previous_balance = OLD.previous_balance
        WHERE id = util_get_next_transaction(OLD.id, OLD.balance_id);
    ELSE
        UPDATE balance
        SET balance = OLD.previous_balance
        WHERE id = OLD.balance_id;
        --changing target balance if transaction is transfer
        IF OLD.type_id = 3 THEN
            UPDATE balance
            SET balance = balance - OLD.amount
            WHERE id = OLD.target_balance_id;
        END IF;
    END IF;
    RETURN OLD;
END; $$
LANGUAGE PLPGSQL;