## Getting Started

This project is a data pipeline which downloads CSV files from a S3 public bucket, applies transformations to it, and loads the data into a Postgres datawarehouse. The data pipeline is hosted in Airflow.

The project is developed in a Docker environment, which fires up all the containers required. 

## Prerequisites

You need to install docker, depending on your environment, follow Docker instructions on https://docs.docker.com/get-docker/. 

If you have a limited RAM memory(8GO or less), you might encounter issues installing airflow, try to allocate as much memory as possible to Docker following those instructions:
https://docs.microsoft.com/en-ie/windows/wsl/wsl-config

Copy docker-compose.yml and Dockerfile to your docker home folder

To install the environment, run in your command line:
> docker-compose up

To check all containers are running and healthy:
> docker ps

You should be able to login to Airflow interface on http://localhost:8080. All credentials are in docker-compose.yml.

## Pipeline installation

- Copy shopify_pipeline.py into Airflow/dags/ folder
- Connect to Airflow Webserver, click on DAG, you should see the DAG listed
- Create a Postgresql connection in Airflow Admin/Connections (id= dwh, type=postgres, host=warehouse, schema=algolia_wh,login=algolia_user, port=5432). Password is provided in docker-compose file. 
- Copy shopify_pipeline_test.py into the home Airflow/ folder.
- If you are under windows, you might need to synchronize the linux container with the Airflow folder. Replace ContainerID with the airflow webserver container ID, which you can find in Docker UI or by running "docker ps":

> Docker cp ..\Airflow\shopify_s3_pipeline_test.py ContainerID:/opt/airflow/shopify_s3_pipeline_test.py

Replace ".." byt the absolute path to your Airflow installation.

## Run unit testing

Connect to airflow:

> docker exec -it airflow-airflow-webserver /bin/bash

Run the unit test script, no error should come up:

>python shopify_pipeline_test.py

## Run the pipeline

To execute the pipeline you can either run it from the UI, or with the command line. Some commands below might differ slightly depending on your OS. 

First, connect to the Airflow webserver, replace airflow-airflow-webserver by your container name(you can find it in Docker UI or by running “docker ps”):

> docker exec -it airflow-airflow-webserver /bin/bash

You should be in the Airflow command line now. To run the full dag:

> airflow dags test shopify_s3_pipeline 2019-04-01

If you want to execute a specific task:

> airflow tasks test shopify_s3_pipeline download_from_s3 2021-04-01

If you want to run the pipeline for a specific date range(dates in the parameters are excluded):
> airflow dags backfill -s 2019-04-01 -e 2019-04-07 shopify_s3_pipeline

POSTRESQL

At this stage, there should be data in the Postgres database. 
Connect to the server:
> docker exec -it  airflow-warehouse psql -U algolia_user algolia_wh

You can then run:

> SELECT * FROM SHOPIFY_CONFIGURATION;

## Logs
