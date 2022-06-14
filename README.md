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

- Copy shopify_pipeline.py into in the DAG folder in your Airflow home folder 
- Connect to Airflow Webserver, click on DAG, you should see the DAG listed
- Copy shopify_pipeline_test.py into
- Copy step to image
- Create a Postgresql connection in Airflow Admin/Connections


## Run the pipeline

To execute the pipeline you can either run it from the UI, or with the command line. Some commands below might differ slightly depending on your OS. 

First, connect to the Airflow webserver, replace airflow-airflow-webserver by your container name(you can find it in Docker UI or by running “docker ps”):

> docker exec -it airflow-airflow-webserver /bin/bash

You should be in the Airflow command line now. To run the full dag:

> airflow dags test shopify_s3_pipeline 2019-04-01

If you want to execute a specific task:

> airflow tasks test shopify_s3_pipeline download_from_s3 2021-04-01

If you want to run the pipeline for a specific date range(dates in the parameters are excluded):
> airflow dags backfill -s 2019-03-31 -e 2019-04-08 shopify_s3_pipeline

POSTRESQL

At this stage, there should be data in the Postgres database. 
Connect to the server:
> docker exec -it  airflow-warehouse psql -U algolia_user algolia_wh

You can then run:

> SELECT * FROM SHOPIFY_CONFIGURATION;

