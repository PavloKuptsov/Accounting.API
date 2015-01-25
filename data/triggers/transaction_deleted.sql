DROP TRIGGER IF EXISTS transaction_deleted ON transaction;

CREATE TRIGGER transaction_deleted
    BEFORE DELETE
    ON transaction
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_transaction_delete();