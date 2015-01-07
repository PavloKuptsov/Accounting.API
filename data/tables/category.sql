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