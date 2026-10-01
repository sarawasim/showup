-- Runs once when the Postgres volume is first created.
-- The backend test suite uses this database so it never touches dev data.
CREATE DATABASE showup_test;
