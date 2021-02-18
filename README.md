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
>>> from post.search import init
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

## Installation for dev server

1. Install docker

```shell
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
sudo apt install docker-ce
```

2. Install docker-compose

```shell
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. Clone the git repository
```shell
cd /var
mkdir www
cd www
git clone git@github.com:mmanylov/django_blog_real.git blog
cd blog
```

4. Add server domain/IP-address to the allowed hosts in .env.dev file

```DJANGO_ALLOWED_HOSTS = <address>```

5. Build and run the containers
```shell
docker-compose -f docker-compose.yml up -d --build
```

6. Migrate the database
```shell
cat dump/2018-05-22.sql | docker exec -i django_blog_real_db_1 psql -U bloguser -W blog
```

7. Create the 'blog' index in Elasticsearch and index posts with init()
```shell
docker-compose -f docker-compose.yml exec web python manage.py shell
>>> from post.search import init
>>> init()
```
