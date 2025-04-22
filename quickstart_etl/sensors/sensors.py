import json
import os

import dagster as dg

from ..jobs.sor_2_jobs import sor_2_job_1, sor_2_job_2, sor_2_job_3, sor_2_job_4
from ..jobs.sor_1_jobs import sor_1_job_1


@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.SUCCESS,
    monitored_jobs=[sor_2_job_1],
    request_job=sor_2_job_3,
    #default_status=dg.DefaultSensorStatus.RUNNING,
)
def sor_2_monitor_job_1_sensor(context: dg.RunStatusSensorContext):
    return dg.RunRequest(run_key=None)


@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.SUCCESS,
    monitored_jobs=[sor_2_job_2, sor_2_job_3],
    request_job=sor_2_job_4,
    #default_status=dg.DefaultSensorStatus.RUNNING,
)
def sor_2_monitor_jobs_sensor(context: dg.RunStatusSensorContext):
    # Check for successful completion of both monitored jobs
    for job in [sor_2_job_2, sor_2_job_3]:
        run_records = context.instance.get_run_records(
            filters=dg.RunsFilter(
                job_name=job.name,
                statuses=[dg.DagsterRunStatus.SUCCESS],
            ),
            order_by="update_timestamp",
            ascending=False,
        )
        # If any job has not completed successfully, skip
        if not run_records:
            return dg.SkipReason(f"Job {job.name} has not completed successfully")

    # If both jobs have succeeded, request a run for sor_2_job_4
    return dg.RunRequest(run_key=None)


# Define the paths to monitor
FOLDER_PATHS = [
    "/Users/izzy/src/zzz_test_serverless_dbt/quickstart_etl/utils/file_1_path",
    "/Users/izzy/src/zzz_test_serverless_dbt/quickstart_etl/utils/file_2_path",
    "/Users/izzy/src/zzz_test_serverless_dbt/quickstart_etl/utils/file_3_path",
    "/Users/izzy/src/zzz_test_serverless_dbt/quickstart_etl/utils/file_4_path",
    "/Users/izzy/src/zzz_test_serverless_dbt/quickstart_etl/utils/file_5_path",
    "/Users/izzy/src/zzz_test_serverless_dbt/quickstart_etl/utils/file_6_path",
]


@dg.sensor(job=sor_1_job_1, minimum_interval_seconds=30)
def new_files_sensor(context: dg.SensorEvaluationContext):
    # Load the last processed timestamps from the cursor
    if context.cursor is None:
        last_processed = {path: 0 for path in FOLDER_PATHS}
    else:
        last_processed = json.loads(context.cursor)

    all_new_files = True
    new_files = {}

    for path in FOLDER_PATHS:
        latest_file_time = last_processed.get(path, 0)
        for filename in os.listdir(path):
            if filename.startswith("file_") and filename.endswith(".csv"):  # Adjust file pattern as needed
                filepath = os.path.join(path, filename)
                file_time = os.path.getmtime(filepath)
                if file_time > latest_file_time:
                    new_files[path] = filename
                    latest_file_time = file_time

        if path not in new_files:
            all_new_files = False

        last_processed[path] = latest_file_time

    if all_new_files:
        # Update the cursor with the latest processed times
        context.update_cursor(json.dumps(last_processed))  # Use json.dumps to serialize
        yield dg.RunRequest(run_key="new_files_detected")
    else:
        yield dg.SkipReason("Not all folders have new files yet.")