DROP TRIGGER IF EXISTS transaction_updated ON transaction;

CREATE TRIGGER transaction_updated
    AFTER UPDATE
    ON transaction
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_transaction_change();