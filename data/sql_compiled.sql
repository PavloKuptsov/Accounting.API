--- TABLES ---


DROP TABLE IF EXISTS transaction CASCADE;

CREATE TABLE transaction (
    id SERIAL PRIMARY KEY,
    type_id INT,
    amount DECIMAL,
    balance_id INT,
    category_id INT,
    comment VARCHAR(255),
    date DATE,
    exchange_rate DECIMAL DEFAULT 1,
    child_to INT DEFAULT NULL
);

CREATE INDEX idx_id_transaction
ON transaction (id);

CREATE INDEX idx_date_transaction
ON transaction (date);


DROP TABLE IF EXISTS tag;

CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);


DROP TABLE IF EXISTS category;

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_category_id INT,
    type_id INT
);

CREATE INDEX idx_id_category
ON category (id);

INSERT INTO category ( id, name, parent_category_id, type_id ) VALUES
    (1, 'Correction', NULL, 1),
    (2, 'Salary', NULL, 2);


DROP TABLE IF EXISTS currency;

CREATE TABLE currency (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    short_name VARCHAR(3)
);

INSERT INTO currency ( id, name, short_name ) VALUES
    (1, 'Ukrainian Hryvna', 'UAH'),
    (2, 'US Dollar', 'USD');
--    (3, 'Euro', 'EUR');


DROP TABLE IF EXISTS account;

CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    type_id INT,
    name VARCHAR(100),
    owner_id INT
);

CREATE INDEX idx_id_account
ON account (id);

INSERT INTO account ( id, type_id, name, owner_id ) VALUES
    (1, NULL, 'Cash', NULL),
    (2, NULL, 'Credit Card', NULL);


DROP TABLE IF EXISTS transaction_type;

CREATE TABLE transaction_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO transaction_type ( id, name ) VALUES
    (1, 'Spending'),
    (2, 'Income'),
    (3, 'Transfer parent'),
    (4, 'Transfer child');


DROP TABLE IF EXISTS balance;

CREATE TABLE balance (
    id SERIAL PRIMARY KEY,
    account_id INT,
    currency_id INT,
    balance DECIMAL
);

CREATE INDEX idx_id_balance
ON balance (id);

INSERT INTO balance ( id, account_id, currency_id, balance ) VALUES
    (1, 1, 1, 2500),
    (2, 1, 2, 500),
    (3, 2, 1, 10000);


--- VIEWS ---


DROP VIEW IF EXISTS transaction_by_date_id;

CREATE VIEW transaction_by_date_id AS
SELECT
    row_number() OVER(ORDER BY balance_id ASC, date ASC, id ASC) AS id,
    date,
    id AS transaction_id,
    balance_id
FROM transaction
ORDER BY balance_id ASC, date ASC, id ASC;


--- PROCEDURES ---


DROP FUNCTION IF EXISTS accounts_list();

CREATE FUNCTION accounts_list()
RETURNS TABLE (
    id INT,
    type_id INT,
    name VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.type_id,
        a.name
    FROM account a;
END;
$$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS currency_get(p_id INT);

CREATE FUNCTION currency_get(
    p_id INT
)
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    short_name VARCHAR(3)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.short_name
    FROM currency c
    WHERE c.id = p_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS account_delete(INT);

CREATE FUNCTION account_delete(
    p_id INT
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM account
    WHERE id = p_id;

    DELETE FROM transaction
    WHERE balance_id IN (
        SELECT id
        FROM balance
        WHERE account_id = p_id);

    DELETE FROM balance
    WHERE account_id = p_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS balance_decrease(INT, DECIMAL);

CREATE FUNCTION balance_decrease(
    p_id INT,
    p_amount DECIMAL
)
RETURNS VOID AS $$
    DECLARE v_balance DECIMAL;
BEGIN
    SELECT balance - p_amount INTO v_balance
    FROM balance
    WHERE id = p_id;

    UPDATE balance
    SET
        balance = v_balance
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;


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


DROP FUNCTION IF EXISTS transactions_list();

CREATE FUNCTION transactions_list()
RETURNS TABLE (
    id INT,
    type_id INT,
    amount DECIMAL,
    balance_id INT,
    category_id INT,
    comment VARCHAR(255),
    date DATE,
    target_balance_id INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id,
        t.type_id,
        t.amount,
        t.balance_id,
        t.category_id,
        t.comment,
        t.date,
        t1.balance_id AS target_balance_id
    FROM transaction t
    LEFT JOIN transaction AS t1 ON t.id = t1.child_to
    WHERE t.type_id != 4
    ORDER BY t.date;
END;
$$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS balance_transaction_reverse_change(INT, DECIMAL, INT);

CREATE FUNCTION balance_transaction_reverse_change(
    p_type_id INT,
    p_amount DECIMAL,
    p_balance_id INT
)
RETURNS void AS $$
BEGIN
    IF p_type_id = 1 OR p_type_id = 3 THEN -- spending or transfer parent
        PERFORM balance_increase(p_balance_id, p_amount);
    ELSIF p_type_id = 2 OR p_type_id = 4 THEN -- income or transfer child
        PERFORM balance_decrease(p_balance_id, p_amount);
    END IF;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS util_get_next_transaction(INT, INT);

CREATE FUNCTION util_get_next_transaction(
    p_id INT,
    p_balance_id INT
)
RETURNS INT AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT a.transaction_id INTO v_id
    FROM (SELECT * FROM transaction_by_date_id WHERE balance_id = p_balance_id) a
    WHERE id = (SELECT id
        FROM transaction_by_date_id
        WHERE transaction_id = p_id
        )+1;
    RETURN v_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS categories_list();

CREATE FUNCTION categories_list()
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    parent_category_id INT,
    type_id INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.parent_category_id,
        c.type_id
    FROM category c;
END;
$$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS balance_get_last_by_date(DATE, INT);

CREATE FUNCTION balance_get_last_by_date(
    p_date DATE,
    p_balance_id INT
)
RETURNS DECIMAL AS $$
DECLARE
    v_balance DECIMAL;
BEGIN
    SELECT INTO v_balance
        CASE t.type_id
            WHEN 2 THEN
                t.previous_balance + t.amount
            ELSE
                t.previous_balance - t.amount
        END
    FROM transaction t
    WHERE t.id = (SELECT MAX(id) FROM transaction WHERE date <= p_date) AND t.balance_id = p_balance_id;
    RETURN v_balance;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS account_change(INT, VARCHAR(50));

CREATE FUNCTION account_change(
    p_id INT,
    p_name VARCHAR(50)
)
RETURNS VOID AS $$
BEGIN
    UPDATE account
    SET
        name = p_name
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS account_get(p_id INT);

CREATE FUNCTION account_get(
    p_id INT
)
RETURNS TABLE (
    id INT,
    type_id INT,
    name VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.type_id,
        a.name
    FROM account a
    WHERE a.id = p_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS transaction_create(INT, DECIMAL, INT, INT, INT, VARCHAR(255), DATE, DECIMAL);

CREATE FUNCTION transaction_create(
    p_type_id INT,
    p_amount DECIMAL,
    p_balance_id INT,
    p_target_balance_id INT,
    p_category_id INT,
    p_comment VARCHAR(255),
    p_date DATE,
    p_rate DECIMAL
)
RETURNS INT AS $$
DECLARE
    v_new_transaction_id INT;
BEGIN
    INSERT INTO transaction (
        type_id,
        amount,
        balance_id,
        category_id,
        comment,
        date,
        exchange_rate,
        child_to
    )
    VALUES (
        p_type_id,
        p_amount,
        p_balance_id,
        p_category_id,
        p_comment,
        p_date,
        p_rate,
        NULL
    )
    RETURNING id INTO v_new_transaction_id;
    PERFORM balance_transaction_change(p_type_id, p_amount, p_balance_id);

    IF (p_type_id = 3)
    THEN
        INSERT INTO transaction (
            type_id,
            amount,
            balance_id,
            category_id,
            comment,
            date,
            exchange_rate,
            child_to
        )
        VALUES (
            4,
            p_amount * p_rate,
            p_target_balance_id,
            NULL,
            NULL,
            p_date,
            1,
            v_new_transaction_id
        )
        RETURNING id INTO v_new_transaction_id;
        PERFORM balance_transaction_change(4, p_amount * p_rate, p_target_balance_id);
    END IF;

    RETURN v_new_transaction_id;
END; $$
LANGUAGE PLPGSQL;


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


DROP FUNCTION IF EXISTS currencies_list();

CREATE FUNCTION currencies_list()
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    short_name VARCHAR(3)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.short_name
    FROM currency c;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS balance_transaction_change(INT, DECIMAL, INT);

CREATE FUNCTION balance_transaction_change(
    p_type_id INT,
    p_amount DECIMAL,
    p_balance_id INT
)
RETURNS void AS $$
BEGIN
    IF p_type_id = 1 OR p_type_id = 3 THEN -- spending or transfer parent
        PERFORM balance_decrease(p_balance_id, p_amount);
    ELSIF p_type_id = 2 OR p_type_id = 4 THEN -- income or transfer child
        PERFORM balance_increase(p_balance_id, p_amount);
    END IF;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS balance_increase(INT, DECIMAL);

CREATE FUNCTION balance_increase(
    p_id INT,
    p_amount DECIMAL
)
RETURNS VOID AS $$
    DECLARE v_balance DECIMAL;
BEGIN
    SELECT balance + p_amount INTO v_balance
    FROM balance
    WHERE id = p_id;

    UPDATE balance
    SET
        balance = v_balance
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS util_get_last_transaction_to_date(INT, DATE);

CREATE FUNCTION util_get_last_transaction_to_date(
    p_balance_id INT,
    p_date DATE
)
RETURNS INT AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT max(a.transaction_id) INTO v_id
    FROM (SELECT * FROM transaction_by_date_id WHERE balance_id = p_balance_id AND date <= p_date) a;
    RETURN v_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS balance_create(INT, INT, DECIMAL);

CREATE FUNCTION balance_create(
    p_account_id INT,
    p_currency_id INT,
    p_balance DECIMAL
)
RETURNS INT AS $$
DECLARE
    v_new_balance_id INT;
BEGIN
    INSERT INTO balance (
        account_id,
        currency_id,
        balance
    )
    VALUES (
        p_account_id,
        p_currency_id,
        p_balance
    )
    RETURNING id INTO v_new_balance_id;
    RETURN v_new_balance_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS account_create(VARCHAR, INT, DECIMAL);

CREATE FUNCTION account_create(
    p_name VARCHAR(50),
    p_default_currency_id INT,
    p_balance DECIMAL
)
RETURNS INT AS $$
DECLARE
    v_new_account_id INT;
BEGIN
    INSERT INTO account (
        name
    )
    VALUES (
        p_name
    )
    RETURNING id INTO v_new_account_id;
    INSERT INTO balance (
        account_id,
        currency_id,
        balance
    )
    VALUES (
        v_new_account_id,
        p_default_currency_id,
        p_balance
    );
    RETURN v_new_account_id;
END; $$
LANGUAGE PLPGSQL;


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


DROP FUNCTION IF EXISTS transaction_delete(INT);

CREATE FUNCTION transaction_delete(
    p_id INT
)
RETURNS BOOL AS $$
    DECLARE
        v_type_id INT;
        v_balance_id INT;
        v_amount DECIMAL;
BEGIN
    SELECT type_id, balance_id, amount INTO v_type_id, v_balance_id, v_amount
    FROM transaction
    WHERE id = p_id;
    PERFORM balance_transaction_reverse_change(v_type_id, v_amount, v_balance_id);

    SELECT type_id, balance_id, amount INTO v_type_id, v_balance_id, v_amount
    FROM transaction
    WHERE child_to = p_id;
    PERFORM balance_transaction_reverse_change(v_type_id, v_amount, v_balance_id);

    DELETE FROM transaction
    WHERE id = p_id;

    DELETE FROM transaction
    WHERE child_to = p_id;
    RETURN TRUE;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS balance_change(INT, DECIMAL);

CREATE FUNCTION balance_change(
    p_id INT,
    p_balance DECIMAL
)
RETURNS VOID AS $$
BEGIN
    UPDATE balance
    SET
        balance = p_balance
    WHERE id = p_id;
END; $$
LANGUAGE PLPGSQL;


--- TRIGGERS ---


