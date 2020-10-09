# musical_instrument_rental
A musical instrument rental system implemented as part of the Software Engineering final assignment at INF-UFRGS

## How to use
Make sure you have all the required python packages installed (`requirements.txt`) and terminal is located in app directory.

### Without docker
You must have a postgres machine to create our database. Then, you should do:

#### Postgres machine:
1. Set `POSTGRES_USER` to postgres user;
2. Set `POSTGRES_PASSWORD` to postgres password;
3. Set `RENTAL_POSTGRES_DB_NAME`;
4. Set `RENTAL_POSTGRES_USER`;
5. Copy `postgres/db-setup.sh` to this machine;
6. Run `postgres/db-setup.sh` in it to create users and tables.

#### Application:
1. Set `RENTAL_DATABASE_HOST` to postgres ip;
2. Set `RENTAL_DATABASE_PORT` to postgres port;
3. Set `RENTAL_DATABASE_DATABASE` to database name;
4. Set `RENTAL_DATABASE_USER` to database user with all privileges;
5. Set `RENTAL_DATABASE_PASSWORD` to database password;
6. Run `make run`.

### With docker

#### Postgres machine:
1. Run `make build-postgres`;
2. Run `make up-postgres`.

#### Application:
1. Set `RENTAL_DATABASE_HOST=localhost`;
2. Set `RENTAL_DATABASE_PORT=5432`
3. Set `RENTAL_DATABASE_DATABASE=music_rental`;
4. Set `RENTAL_DATABASE_USER=rental_admin`;
5. Set `RENTAL_DATABASE_PASSWORD=password`;
6. Run `make run`.
