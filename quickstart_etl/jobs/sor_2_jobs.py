import dagster as dg

sor_2_job_1 = dg.define_asset_job(
    name="sor_2_job_1",
    selection=dg.AssetSelection.assets("asset_18")
)

sor_2_daily_schedule_1 = dg.ScheduleDefinition(
    job=sor_2_job_1,
    cron_schedule="0 0 * * *",  # Cron expression for midnight
)

sor_2_job_2 = dg.define_asset_job(
    name="sor_2_job_2",
    selection=dg.AssetSelection.assets("asset_19")
)

sor_2_job_3 = dg.define_asset_job(
    name="sor_2_job_3",
    selection=dg.AssetSelection.assets("asset_20")
)

sor_2_job_4 = dg.define_asset_job(
    name="sor_2_job_4",
    selection=dg.AssetSelection.assets("asset_21")
)

