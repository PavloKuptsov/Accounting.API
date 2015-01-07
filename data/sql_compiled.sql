--- TABLES ---


DROP TABLE IF EXISTS transaction;

CREATE TABLE transaction (
    id SERIAL PRIMARY KEY,
    type_id INT,
    amount DECIMAL,
    balance_id INT,
    target_balance_id INT,
    previous_balance DECIMAL,
    category_id INT,
    comment VARCHAR(255),
    date DATE
);

GRANT ALL ON transaction TO accounting;


DROP TABLE IF EXISTS account;

CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    type_id INT,
    name VARCHAR(100),
    owner_id INT,
    default_currency_id INT
);

INSERT INTO account ( id, type_id, name, owner_id, default_currency_id ) VALUES
    (1, NULL, 'Cash', NULL, 1);

GRANT ALL ON account TO accounting;


DROP TABLE IF EXISTS transaction_type;

CREATE TABLE transaction_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO transaction_type ( id, name ) VALUES
    (1, 'Spending'),
    (2, 'Income'),
    (3, 'Transfer');

GRANT ALL ON transaction_type TO accounting;


DROP TABLE IF EXISTS tag;

CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

GRANT ALL ON tag TO accounting;


DROP TABLE IF EXISTS currency;

CREATE TABLE currency (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    short_name VARCHAR(3),
    exchange_rate DECIMAL
);

INSERT INTO currency ( id, name, short_name, exchange_rate ) VALUES
    (1, 'Ukrainian Hryvna', 'UAH', 1),
    (2, 'US Dollar', 'USD', 15);

GRANT ALL ON currency TO accounting;


DROP TABLE IF EXISTS category;

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_category_id INT,
    type_id INT
);

INSERT INTO category ( id, name, parent_category_id, type_id ) VALUES
    (1, 'All', NULL, 1),
    (2, 'All', NULL, 2),
    (3, 'Correction', 1, 1),
    (4, 'Salary', 2, 2);

GRANT ALL ON account TO accounting;


DROP TABLE IF EXISTS balance;

CREATE TABLE balance (
    id SERIAL PRIMARY KEY,
    account_id INT,
    currency_id INT,
    balance DECIMAL
);

INSERT INTO balance ( id, account_id, currency_id, balance ) VALUES
    (1, 1, 1, 0),
    (2, 1, 2, 500);

GRANT ALL ON balance TO accounting;


--- PROCEDURES ---


DROP FUNCTION IF EXISTS balance_transaction_change(INT, DECIMAL, INT, INT, DECIMAL);

CREATE FUNCTION balance_transaction_change(
    p_type_id INT,
    p_amount DECIMAL,
    p_balance_id INT,
    p_target_balance_id INT,
    p_previous_balance DECIMAL
)
RETURNS void AS $$
DECLARE
    v_currency_id INT;
BEGIN
    IF p_type_id = 1 THEN
        UPDATE balance
        SET balance = p_previous_balance - p_amount
        WHERE id = p_balance_id;
    ELSIF p_type_id = 2 THEN
        UPDATE balance
        SET balance = p_previous_balance + p_amount
        WHERE id = p_balance_id;
    ELSE
        SELECT currency_id INTO v_currency_id
        FROM balance
        WHERE id = p_balance_id;

        UPDATE balance
        SET balance = p_previous_balance - p_amount
        WHERE id = p_balance_id;

        UPDATE balance
        SET balance = p_previous_balance + p_amount
        WHERE id = p_target_balance_id;
    END IF;
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
    WHERE b.account_id = p_account_id;
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
    short_name VARCHAR(3),
    exchange_rate DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.short_name,
        c.exchange_rate
    FROM currency c;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS transaction_create(INT, DECIMAL, DECIMAL, INT, INT, INT, VARCHAR(255), DATE);

CREATE FUNCTION transaction_create(
    p_type_id INT,
    p_amount DECIMAL,
    p_previous_balance DECIMAL,
    p_balance_id INT,
    p_target_balance_id INT,
    p_category_id INT,
    p_comment VARCHAR(255),
    p_date DATE
)
RETURNS INT AS $$
DECLARE
    v_new_transaction_id INT;
BEGIN
    INSERT INTO transaction (
        type_id,
        amount,
        target_balance_id,
        previous_balance,
        balance_id,
        category_id,
        comment,
        date
    )
    VALUES (
        p_type_id,
        p_amount,
        p_target_balance_id,
        p_previous_balance,
        p_balance_id,
        p_category_id,
        p_comment,
        p_date
    )
    RETURNING id INTO v_new_transaction_id;

    PERFORM balance_transaction_change(p_type_id, p_amount, p_balance_id, p_target_balance_id, p_previous_balance);

    RETURN v_new_transaction_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS accounts_list();

CREATE FUNCTION accounts_list()
RETURNS TABLE (
    id INT,
    type_id INT,
    name VARCHAR(100),
    default_currency_id INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.type_id,
        a.name,
        a.default_currency_id
    FROM account a;
END;
$$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS account_create(VARCHAR, INT);

CREATE FUNCTION account_create(
    p_name VARCHAR(50),
    p_default_currency_id INT
)
RETURNS INT AS $$
DECLARE
    v_new_account_id INT;
BEGIN
    INSERT INTO account (
        name,
        default_currency_id
    )
    VALUES (
        p_name,
        p_default_currency_id
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
        0
    );
    RETURN v_new_account_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS account_get(p_id INT);

CREATE FUNCTION account_get(
    p_id INT
)
RETURNS TABLE (
    id INT,
    type_id INT,
    name VARCHAR(100),
    default_currency_id INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.type_id,
        a.name,
        a.default_currency_id
    FROM account a
    WHERE a.id = p_id;
END; $$
LANGUAGE PLPGSQL;


DROP FUNCTION IF EXISTS currency_get(p_id INT);

CREATE FUNCTION currency_get(
    p_id INT
)
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    short_name VARCHAR(3),
    exchange_rate DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.short_name,
        c.exchange_rate
    FROM currency c
    WHERE c.id = p_id;
END; $$
LANGUAGE PLPGSQL;


