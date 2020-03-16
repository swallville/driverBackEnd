#!/bin/bash

set -e

sudo docker exec -it db_postgres psql -U postgres -c \
"CREATE ROLE ${1} LOGIN ENCRYPTED PASSWORD '${2}' \
SUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;" \

sudo docker exec -it db_postgres psql -U postgres -c \
"ALTER ROLE ${1} WITH SUPERUSER CREATEDB VALID UNTIL 'infinity'; \
ALTER USER ${1} SUPERUSER CREATEDB;" \

echo "Type the name of your database, followed by [ENTER]:"
read DATABASE

sudo docker exec -it db_postgres psql -U postgres -c \
"CREATE DATABASE ${3} WITH OWNER = ${1} \
ENCODING = 'UTF8' TABLESPACE = pg_default LC_COLLATE = 'pt_BR.UTF-8' \
LC_CTYPE = 'pt_BR.UTF-8' CONNECTION LIMIT = -1 TEMPLATE template0;" \

sudo docker exec -it db_postgres psql -U postgres -c \
"CREATE EXTENSION IF NOT EXISTS postgis;" \
