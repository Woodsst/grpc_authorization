# grpc_authorization
## Hello! that's small simple authorization server based on gRPC and PostgreSQL. That server worked with messanger: https://github.com/Woodsst/messanger_grpc
## Requirements:
### requirements.txt in root

* python 3.9 +
* Postgres 12 +
* docker
* grpcio == 1.46.0
* grpcio-tools == 1.46.0
* pytest == 7.1.2
* psycopg == 3.0.12
* psycopg-binary == 3.0.12
* psutil~=5.9.0
* pyYAML==6.0
* PyJWT~=2.4.0

## all config for connect with database and key for jwt in config.yml
```
db_host: database
db_name: messanger
db_password: '123'
db_port: 5432
db_username: wood
secret_key: secret_key
```
### For test - docker-compose-def file
```
$ docker-compose -f docker-compose-dev.yml -p test up
```
That command create and run container for tests
### For stable version
```
$ doocker-compose -f docker-compose.yml up
```
That command create and run container for server and PosgreSQL

## Soon(or not) there will be a messenger client here
