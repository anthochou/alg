from airflow.models import DagBag
import pendulum

#DAG INTEGRITY TEST
def test_no_import_errors():
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id='shopify_s3_pipeline') 
    assert len(dag_bag.import_errors) == 0, "No Import Failures"
    assert dag is not None

#DAG PARAMETERS TESTING
def test_dag_parameters():
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id='shopify_s3_pipeline') 
    assert dag.start_date == pendulum.datetime(2019, 4, 1)
    assert dag.end_date == pendulum.datetime(2019, 4, 7)

#TO DO
#DAG TASKS ORDER
#TASK TESTING(check a file exists after download task)

#TESTING
test_no_import_errors()
test_dag_parameters()