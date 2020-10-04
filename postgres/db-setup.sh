#!/bin/bash
set -e

if [ -z "${POSTGRES_PASSWORD}" ]; then
    echo "Setting default password for user ${RENTAL_POSTGRES_USER}"
    POSTGRES_PASSWORD=password
fi

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -c "CREATE DATABASE ${RENTAL_POSTGRES_DB_NAME};"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -c "CREATE USER ${RENTAL_POSTGRES_USER} WITH SUPERUSER PASSWORD '${POSTGRES_PASSWORD}';"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -c "GRANT ALL PRIVILEGES ON DATABASE ${RENTAL_POSTGRES_DB_NAME} TO ${RENTAL_POSTGRES_USER};"

psql -v ON_ERROR_STOP=1 --username "$RENTAL_POSTGRES_USER" --dbname "$RENTAL_POSTGRES_DB_NAME" <<-EOSQL
    CREATE ROLE readaccess;

    GRANT USAGE ON SCHEMA public TO readaccess;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO readaccess;

    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readaccess;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$RENTAL_POSTGRES_USER" --dbname "$RENTAL_POSTGRES_DB_NAME" <<-EOSQL
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        email VARCHAR NOT NULL UNIQUE,
        password VARCHAR NOT NULL
    );
EOSQL