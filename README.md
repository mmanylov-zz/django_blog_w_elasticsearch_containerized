# General Information

This project is a single user blog app written in python 3.6 using Django, Gunicorn with Nginx, Elasticsearch and React.

## Deployment

Below is a set of instructions to deploy the project.

You could follow the following [tutorial on DO](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) to set up a server without Elasticsearch and React.

Elasticsearch installation and configuration process is described in section **Install and Configure Elasticsearch**.

React installation and configuration process is described in section **Install and Configure React**.

### Prerequisites

In order to complete this guide, you should have a fresh Ubuntu 18.04 server instance with a non-root user with sudo privileges configured. You can learn how to set this up by running through our [initial server setup guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04).

### First Install Python 3

`
sudo apt-get update
sudo apt-get install python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx
`

### Create a Python Virtual Environment for your Project

I prefer to use native python3 venv utility to create venvs:
`python3 -m venv <vevn name here>`

Before we install our project's Python requirements, we need to activate the virtual environment. You can do that by typing:
`source <vevn name here>/bin/activate`

With your virtual environment active, install all the dependencies:
`pip install -r requirements.txt`

### Create the PostgreSQL Database and User

Log into an interactive Postgres session by typing:
`sudo -u postgres psql`

First, create a database for your project:
`CREATE DATABASE myproject;`

Next, create a database user for our project. Make sure to select a secure password:
`CREATE USER myprojectuser WITH PASSWORD 'password';`

Afterwards, we'll modify a few of the connection parameters for the user we just created. This will speed up database operations so that the correct values do not have to be queried and set each time a connection is established.

We are setting the default encoding to UTF-8, which Django expects. We are also setting the default transaction isolation scheme to "read committed", which blocks reads from uncommitted transactions. Lastly, we are setting the timezone. By default, our Django projects will be set to use UTC. These are all recommendations from the Django project itself:
`ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';`

Now, we can give our new user access to administer our new database:
`GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;`

When you are finished, exit out of the PostgreSQL prompt by `CTRL+d` or typing `\q`.


### Rsstore Development Database And Test the Setup

Run the following command from the **dump** directory:
`psql -U bloguser -h localhost -W blog < 2018-05-22.sql`

**Don't forget to change database user and password in project settings according to your setup!**

Project settings are in blog/settings.py file.

There can be some new migrations that were published by django maintaners team so you should run the following command before running the app:
`python manage.py migrate`

### Run Development Server

Anyway, if you deploy for development needs you can try run in your project directory
`python manage.py runserver`
and the sc	
Set the minimum and maximum heap size to 4000 MB.ript will tell you that there are some unaplied migrations.

### Install and Configure Elasticsearch


NOTICE:
Elasticsearch needs 1Gb of RAM to start, so if you don't have so much free RAM on your machine or don't want the Elasticsearch to borrow so much system memory, you can change the Elasticsearch configuration. See [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html) from more information.

I had to make these changes in:

`/etc/elasticsearch/jvm.options`


\# Xms represents the initial size of total heap space
\# Xmx represents the maximum size of total heap space

-Xms1g 
-Xmx1g 
\# the settings shipped with ES 5 were: -Xms2g
\# the settings shipped with ES 5 were: -Xmx2g
`

Set the minimum and maximum heap size to 2 GB.
`ES_JAVA_OPTS="-Xms2g -Xmx2g" ./bin/elasticsearch`
	
Set the minimum and maximum heap size to 4000 MB.
`ES_JAVA_OPTS="-Xms4000m -Xmx4000m" ./bin/elasticsearch`


Reference
[all systems](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
[Ubuntu](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html)

Download and install

`
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.3.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.3.deb.sha512
shasum -a 512 -c elasticsearch-6.2.3.deb.sha512 
sudo dpkg -i elasticsearch-6.2.3.deb
`

Configure the service with systemd
`
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
`

Run the service
`
sudo service elasticsearch start
sudo service elasticsearch stop
`

Get status with
`
sudo service elasticsearch status
`

See logs in `/var/log/elasticsearch/`.

Test it
`
curl -XGET 'localhost:9200/?pretty'
`

### Create Elasticsearch Index and Import Database Data

All the needed commands are already implemented in `post/search.py` file.


To crate an index and index the database use project intercative shell
`python manage.py shell`

Include the needed file to create the index and index th data from the DB:
`>>> from post.search import *`

Run the indexing command:
`>>> bulk_indexing()`

To drop the index run:
`>>> drop_index()`

To search run
`>>> search(query)`
where query is a string to find in title, excerpt or body of a post.


[Tutorial](https://medium.freecodecamp.org/elasticsearch-with-django-the-easy-way-909375bc16cb
https://github.com/elastic/elasticsearch-dsl-py
) I foollowed to create the Elasticsearch connection with Django app.

In the project I use Elasticsearch DSL library for simplicity sake.
[Elasticsearch DSL manual](https://elasticsearch-dsl.readthedocs.io/en/latest/)

## Project Settings

Project settings are in blog/settings.py file.


