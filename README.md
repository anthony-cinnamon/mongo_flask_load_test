# Flask mongo load and consistent test

## Components

1. flaskr: Flask app contains logic to query MongoDB server with very simple
      object: People
2. mongo_cluster: Dockerfile for create 3-node replica set
3. tests: Test suite written in locust

## Bring up flask

```bash
docker build -t flask_test .
```

## Setup mongodb cluster

1. Use docker-compose file to bring up 3-node cluster
2. Init replica set:

```bash
docker exec  mongo1 mongo /docker-entrypoint-initdb.d/init_rs.js
```