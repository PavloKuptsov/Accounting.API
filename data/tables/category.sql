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