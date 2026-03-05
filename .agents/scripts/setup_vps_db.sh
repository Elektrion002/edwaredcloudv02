#!/bin/bash
set -e

echo "Setting up PostgreSQL user and database..."
sudo -u postgres psql -c "CREATE USER edwared_admin WITH PASSWORD 'MEwar3x4-12VpS';" || true
sudo -u postgres psql -c "CREATE DATABASE edwared_master OWNER edwared_admin;" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE edwared_master TO edwared_admin;"
sudo -u postgres psql -c "ALTER USER edwared_admin CREATEDB;"

echo "Database edwared_master and user edwared_admin have been set up."

# Also ensuring listen_addresses = 'localhost' is configured in postgresql.conf
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/g" /etc/postgresql/16/main/postgresql.conf || true
echo "Restarting PostgreSQL..."
systemctl restart postgresql
echo "Finished!"
