from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)
from dagster_dbt import DbtCliResource

from . import assets
from .project import jaffle_shop
from .assets.google_sheets import google_sheets_resource

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), cron_schedule="0 0 * * *"
)

defs = Definitions(
    assets=load_assets_from_package_module(assets),
    schedules=[daily_refresh_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=jaffle_shop),
        "google_sheets": google_sheets_resource,
    },
)
