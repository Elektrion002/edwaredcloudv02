DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE  rolname = 'edwared_admin') THEN
      CREATE ROLE edwared_admin LOGIN PASSWORD 'MEwar3x4-12VpS';
   END IF;
END
$do$;
ALTER USER edwared_admin WITH PASSWORD 'MEwar3x4-12VpS';
ALTER ROLE edwared_admin CREATEDB;
DROP DATABASE IF EXISTS edwared_master;
CREATE DATABASE edwared_master OWNER edwared_admin;
GRANT ALL PRIVILEGES ON DATABASE edwared_master TO edwared_admin;
