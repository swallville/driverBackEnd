driverBackEnd
====

Driver DRF Example Backend developed by Lukas F. Machado.

Setup Development Environment Docker
------------------------------------
- Install Docker and Docker Compose
  - `$ sudo make up-postgres-dev`
 
- Create database
  - `$ make create_default_db`
  - When prompted, enter the name of the database
    as `driverbackend`.

- Setup `.env` file on the following structure:
```
SECRET_KEY=+m=lh4bc!=_t2_31231221332DSSADadsasasdasd32132p(3lgz5*81#mph
DEBUG=True
DATABASE_URL=postgis://driverbackend:driverbackend@db_postgres:5432/driverbackend
ALLOWED_HOSTS=*
CORS_ORIGIN_WHITELIST=*
````

- Build api container
  - `$ sudo make build-api-dev`

- Setup `.env` file inside the dockerfiles directory on the following structure:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
````

- Run api container
  - `$ sudo docker-compose run --service-ports api`

- Enter inside Docker Machine
  - `$ sudo make ssh-api`
  - `$ sudo make ssh-postgres`

- Create super user inside the Django REST API container
  - `$ sudo make createsuperuser`

Running Tests
----------------------
-  Run all tests cases
    - `$ sudo make test`

-  Run a single App tests cases
    - `$ sudo make test_module`

Some Docker operations
----------------------
**Stop containers**
```
$ sudo docker stop $(sudo docker ps -a -q)
```

**Remove containers**
```
$ sudo docker rm $(sudo docker ps -a -q)
```

**Remove all images**
```
$ sudo docker rmi $(sudo docker images -q)
```

**Prune containers**
```
$ sudo docker system prune
$ sudo docker system prune --volumes
```
