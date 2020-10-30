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

    CREATE TABLE instruments (
        id VARCHAR PRIMARY KEY,
        class VARCHAR NOT NULL,
        instrument VARCHAR NOT NULL,
        brand VARCHAR NOT NULL,
        model VARCHAR NOT NULL,
        registry VARCHAR NOT NULL
    );

    CREATE TABLE adverts_data (
        id VARCHAR PRIMARY KEY,
        prices VARCHAR NOT NULL,
        locator VARCHAR NOT NULL REFERENCES users(email),
        instrument VARCHAR NOT NULL REFERENCES instruments(id)
    );

    CREATE TABLE adverts (
        id SERIAL PRIMARY KEY,
        active BOOL NOT NULL DEFAULT TRUE,
        data VARCHAR NOT NULL UNIQUE REFERENCES adverts_data(id)
    );

    CREATE TABLE loans (
        id VARCHAR PRIMARY KEY,
        withdrawal DATE NOT NULL,
        devolution DATE NOT NULL,
        lessee VARCHAR NOT NULL REFERENCES users(email),
        ad VARCHAR NOT NULL REFERENCES adverts(data)
    );

    CREATE TABLE records (
        id SERIAL PRIMARY KEY,
        loan VARCHAR NOT NULL REFERENCES loans(id),
        rating INT NOT NULL CONSTRAINT rating_interval CHECK (rating >= 0 AND rating <= 10)
    );
EOSQL