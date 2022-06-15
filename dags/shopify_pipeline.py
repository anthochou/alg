import os
import boto3
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from botocore import UNSIGNED
from botocore.client import Config

def download_from_s3(s3_object: str, bucket_name: str):
    #Downloads file from the S3 bucket based on dag execution date    

    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    s3.download_file(bucket_name,s3_object, s3_object )
   
def transform (s3_object: str):
    # Applies the 2 transformations to the file: filter + new column

    import pandas as pd
    import numpy as np

    df = pd.read_csv(s3_object, skip_blank_lines=True)
    df = df[df['application_id'].notnull()]
    df['has_specific_prefix'] = np.where(df['index_prefix'] == 'shopify_', False, True)
    df.to_csv(s3_object, index = False)

def load_dwh (s3_object: str):
    #Loads the valid rows into the dwh

    postgres_hook = PostgresHook(postgres_conn_id="dwh")
    conn = postgres_hook.get_conn()
    cur = conn.cursor()
    
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS "SHOPIFY_CONFIGURATION"
    (
    id TEXT,
    shop_domain TEXT,
    application_id TEXT,
    autocomplete_enabled TEXT,
    user_created_at_least_one_qr TEXT,
    nbr_merchandised_queries TEXT,
    nbrs_pinned_items TEXT,
    showing_logo TEXT,
    has_changed_sort_orders TEXT,
    analytics_enabled TEXT,
    use_metafields TEXT,
    nbr_metafields TEXT,
    use_default_colors TEXT,
    show_products TEXT,
    instant_search_enabled TEXT,
    instant_search_enabled_on_collection TEXT,
    only_using_faceting_on_collection TEXT,
    use_merchandising_for_collection TEXT,
    index_prefix TEXT,
    indexing_paused TEXT,
    install_channel TEXT,
    export_date TEXT,
    has_specific_prefix TEXT
    );'''

    cur.execute(create_table_query)
 
    f = open(s3_object, 'r')
    cur.copy_expert("COPY SHOPIFY_CONFIGURATION FROM STDIN WITH CSV HEADER", f )
    f.close()    

    conn.commit()
    cur.close() 

with DAG(
    dag_id='shopify_s3_pipeline',
    schedule_interval='@daily',
    start_date=datetime(2019, 4, 1),
    end_date=datetime(2019, 4, 7),
    catchup=False,
    # Limited active dag run to 1 because of memory limitation. You can try to remove it to use parallelism.
    max_active_runs=1
) as dag:

    task_download_from_s3 = PythonOperator(
       		task_id='download_from_s3',
	        python_callable=download_from_s3,
	        op_kwargs={
        	    's3_object': '{{ ds }}.csv',
	            'bucket_name': 'alg-data-public'
        	}
	)

    task_transform = PythonOperator(
        	task_id='transform',
	        python_callable=transform,
	        op_kwargs={
        	    's3_object': '{{ ds }}.csv'
        	}
	)

    task_load_dwh = PythonOperator(
        	task_id='load_dwh',
	        python_callable=load_dwh,
	        op_kwargs={
        	    's3_object': '{{ ds }}.csv'
        	}
	)

    task_download_from_s3 >> task_transform >> task_load_dwh 