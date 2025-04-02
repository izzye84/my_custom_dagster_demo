from dagster import asset
from dagster_dbt import get_asset_key_for_model

from .dbt_assets import my_dbt_assets

@asset(deps={get_asset_key_for_model([my_dbt_assets],'my_fifth_model')},
       kinds={'duckdb'})
def some_downstream_asset():
    return [1,2,3]