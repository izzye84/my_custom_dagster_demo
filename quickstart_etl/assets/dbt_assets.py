from typing import Any, Optional
from collections.abc import Mapping

from dagster import AssetExecutionContext, AutomationCondition
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator


from ..project import jaffle_shop


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
        def get_automation_condition(
            self, dbt_resource_props: Mapping[str, Any]
        ) -> Optional[AutomationCondition]:
            return AutomationCondition.eager()
        

@dbt_assets(manifest=jaffle_shop.manifest_path,
            dagster_dbt_translator=CustomDagsterDbtTranslator())
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()