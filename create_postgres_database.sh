#!/bin/bash

set -e

echo "Type the name of your database user, followed by [ENTER]:"
read USERNAME

echo "Type your user's password, followed by [ENTER]:"
read -s PASSWORD

sudo docker exec -it db_postgres psql -U postgres -c \
"CREATE ROLE ${USERNAME} LOGIN ENCRYPTED PASSWORD '${PASSWORD}' \
SUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;" \

sudo docker exec -it db_postgres psql -U postgres -c \
"ALTER ROLE ${USERNAME} WITH SUPERUSER CREATEDB VALID UNTIL 'infinity'; \
ALTER USER ${USERNAME} SUPERUSER CREATEDB;" \

echo "Type the name of your database, followed by [ENTER]:"
read DATABASE

sudo docker exec -it db_postgres psql -U postgres -c \
"CREATE DATABASE ${DATABASE} WITH OWNER = ${USERNAME} \
ENCODING = 'UTF8' TABLESPACE = pg_default LC_COLLATE = 'pt_BR.UTF-8' \
LC_CTYPE = 'pt_BR.UTF-8' CONNECTION LIMIT = -1 TEMPLATE template0;" \

sudo docker exec -it db_postgres psql -U postgres -c \
"CREATE EXTENSION IF NOT EXISTS postgis;" \
