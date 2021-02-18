# Instructions

## Development using Docker

To build dev containers run
```shell
docker-compose -f docker-compose.yml up -d --build
docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
```

To destroy dev containers
```shell
docker-compose -f docker-compose.yml down -v
```

To see logs
```shell
docker-compose -f docker-compose.yml logs -f
```

To see logs of a specific container
```shell
docker logs - f <container name>
```

To see all containers
```shell
docker ps -a
```

For initialization (database creation and applying migrations; creation of es index and bulk indexing of posts from the db)
```shell
cat dump/2018-05-22.sql | docker exec -i django_blog_real_db_1 psql -U bloguser -W blog
docker-compose -f docker-compose.yml exec web python manage.py shell
>>> from search import init
>>> init()
```

Collect static files with
```shell
docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
```

## Production deployment

To build run
```shell
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```
