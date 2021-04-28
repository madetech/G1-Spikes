# Local Deployment

To get started with the local deployment run:

```bash
./setup.sh
```

The script will install a version of Wagtail, and create an initial app. It will then update the Wagtail files to work with PostgreSQL, and create the necessary Docker Containers.
It will also create a Super User admin.

When finished running, Wagtail can be accessed through:

```bash
localhost:8000
```

After the initial setup you can use docker-compose to spin up, or down the containers:

```bash
docker-compose up
```

```bash
docker-compose down
```

 If you make any changes to the wagtail files you will need to rebuild the Wagtail containter, be sure to use the "no-cache" flag so that the updated files are pulled in correctly. 

 ```bash
docker-compose build --no-cache
 ```

## Default Environment Values:
The default Environment Values are used by Wagtail to connect to the Postgres Databases, and passed in through the Docker-Compose file. 
### .env.dev

|Key| Default Value| Description|
|---|---|---|
|DJANGO_SUPERUSER_PASSWORD| admin| Password for Wagtail Admin User|
|DJANGO_SUPERUSER_USERNAME| admin | Username for Wagtail Admin User|
|DJANGO_SUPERUSER_EMAIL| admin@test.com| Email for Wagtail Admin User|
|DEBUG| True | Set to False if want to turn Debug mode off |
|SECRET_KEY|p-3r5as^ls$g42^yoxl56$5h%ct!d!puspdl_p754ca$8ssh6$| Example Key|
|DJANGO_ALLOWED_HOSTS|localhost 127.0.0.1 [::1]| |
|SQL_ENGINE|django.db.backends.postgresql_psycopg2|  |
|SQL_DATABASE|demo_wagtail| |
|SQL_USER|demouser| |
|SQL_PASSWORD|DemoPass| |
|SQL_HOST|db| |
|SQL_PORT|5432| | 
|DATABASE|postgres| |

### .env.db
|Key|Default Value|
|---|---|
|POSTGRES_USER|demouser|
|POSTGRES_PASSWORD|DemoPass|
|POSTGRES_DB|demo_wagtail|