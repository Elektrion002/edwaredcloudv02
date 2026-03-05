#!/bin/bash
# Script to setup the Rewards Program database on the VPS
DB_NAME="edwared_recompensas"
DB_USER="edwared_admin" # Using the same admin user created previously

sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "Database $DB_NAME created and privileges granted to $DB_USER."
