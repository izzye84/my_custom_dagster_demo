import dagster as dg

import holidays


# Create a set of US holidays
us_holidays = holidays.US()

# Function to check if a date is in custom calendar (e.g., US holidays)
def is_not_holiday(context):
    eval_date = context.scheduled_execution_time.date()
    if eval_date in us_holidays:
        holiday_name = us_holidays.get(eval_date)
        context.log.info(f"Skipping execution on {eval_date} because it's {holiday_name}")
        return False
    return True


sor_1_job_1 = dg.define_asset_job(
    name="sor_1_job_1",
    selection=dg.AssetSelection.assets("asset_1", "asset_2", "asset_3", "asset_4", "asset_5", "asset_6")
)

sor_1_daily_schedule_1 = dg.ScheduleDefinition(
    job=sor_1_job_1,
    cron_schedule="0 0 * * *",  # Cron expression for midnight
)


sor_1_job_2 = dg.define_asset_job(
    name="sor_1_job_2",
    selection=dg.AssetSelection.assets("asset_7").downstream()
)

sor_1_daily_schedule_2 = dg.ScheduleDefinition(
    job=sor_1_job_2,
    cron_schedule="0 0 * * *",  # Cron expression for midnight
    should_execute=is_not_holiday
)


sor_1_job_3 = dg.define_asset_job(
    name="sor_1_job_3",
    selection=dg.AssetSelection.assets("asset_17")
)

sor_1_daily_schedule_3 = dg.ScheduleDefinition(
    job=sor_1_job_3,
    cron_schedule="0 0 * * *",  # Cron expression for midnight
)