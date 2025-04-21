from dagster import (
    Definitions,
    load_assets_from_package_module,
)
from dagster_dbt import DbtCliResource

from . import assets
from .project import jaffle_shop
from .assets.google_sheets import google_sheets_resource
from .jobs.sor_1_jobs import (
    sor_1_job_1,
    sor_1_job_2,
    sor_1_job_3,
    sor_1_daily_schedule_1,
    sor_1_daily_schedule_2,
    sor_1_daily_schedule_3
)
from .jobs.sor_2_jobs import sor_2_job_1, sor_2_job_2, sor_2_job_3, sor_2_daily_schedule_1
from .sensors.sensors import sor_2_monitor_job_1_sensor, sor_2_monitor_jobs_sensor, new_files_sensor


defs = Definitions(
    assets=load_assets_from_package_module(assets),
    jobs=[sor_1_job_1, sor_1_job_2, sor_1_job_3, sor_2_job_1, sor_2_job_2, sor_2_job_3],
    schedules=[sor_1_daily_schedule_1, sor_1_daily_schedule_2, sor_1_daily_schedule_3, sor_2_daily_schedule_1],
    sensors=[sor_2_monitor_job_1_sensor, sor_2_monitor_jobs_sensor, new_files_sensor],
    resources={
        "dbt": DbtCliResource(project_dir=jaffle_shop),
        "google_sheets": google_sheets_resource,
    },
)
