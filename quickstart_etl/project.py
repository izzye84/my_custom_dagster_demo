from pathlib import Path

from dagster_dbt import DbtProject

jaffle_shop = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "jaffle_shop").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "dbt-project").resolve(),
)
jaffle_shop.prepare_if_dev()