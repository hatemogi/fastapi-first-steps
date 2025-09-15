CREATE TYPE item_color AS ENUM ('red', 'green', 'blue');

CREATE TABLE items (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    color item_color NOT NULL
);

INSERT INTO items (id, name, color) VALUES
    ('qRhBXnpry7', '아이템A', 'red'),
    ('cOPAmgTBfc', '아이템B', 'green');
