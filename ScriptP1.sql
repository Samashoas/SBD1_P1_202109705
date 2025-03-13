CREATE TABLE test_table (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(50)
);

INSERT INTO test_table (id, name) VALUES (1, 'Test Name');
INSERT INTO test_table (id, name) VALUES (2, 'Test Name 2');
INSERT INTO test_table (id, name) VALUES (3, 'Test Name 3');
INSERT INTO test_table (id, name) VALUES (4, 'Test Name 4');

SELECT * FROM test_table;