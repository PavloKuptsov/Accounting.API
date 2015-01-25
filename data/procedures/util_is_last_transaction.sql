DROP FUNCTION IF EXISTS util_is_last_transaction(INT, INT);

CREATE FUNCTION util_is_last_transaction(
    p_id INT,
    p_balance_id INT
)
RETURNS BOOL AS $$
DECLARE
    v_id INT;
    v_result BOOL;
BEGIN
    SELECT * INTO v_id
    FROM util_get_next_transaction(p_id, p_balance_id);
    IF v_id IS NULL THEN
        v_result = TRUE;
      ELSE v_result = FALSE;
    END IF;
    RETURN v_result;
END; $$
LANGUAGE PLPGSQL;