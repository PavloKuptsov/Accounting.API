DROP FUNCTION IF EXISTS trigger_transaction_change() CASCADE;

CREATE FUNCTION trigger_transaction_change()
RETURNS trigger AS $$
DECLARE
    v_transaction_amount_id DECIMAL;
BEGIN
    IF NEW.type_id = 2 THEN
        v_transaction_amount_id = NEW.amount;
    ELSE v_transaction_amount_id = -(NEW.amount);
    END IF;
    UPDATE transaction
    SET previous_balance = NEW.previous_balance + v_transaction_amount_id
    WHERE id = util_get_next_transaction(NEW.id, NEW.balance_id);
    IF (SELECT * FROM util_is_last_transaction(NEW.id, NEW.balance_id))
    THEN
        UPDATE balance
        SET balance = NEW.previous_balance + v_transaction_amount_id
        WHERE id = NEW.balance_id;
    END IF;
    IF NEW.type_id = 3 THEN
        UPDATE balance
        SET balance = balance - OLD.amount
        WHERE id = OLD.target_balance_id;
        UPDATE balance
        SET balance = balance + NEW.amount
        WHERE id = NEW.target_balance_id;
    END IF;
    RETURN NEW;
END; $$
LANGUAGE PLPGSQL;