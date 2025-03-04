from setuptools import find_packages, setup

setup(
    name="quickstart_etl",
    packages=find_packages(exclude=["quickstart_etl_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "boto3",
        "pandas",
        "matplotlib",
        "textblob",
        "tweepy",
        "wordcloud",
        "dagster-dbt",
        "dbt-duckdb",
        "google-auth",
        "google-api-python-client",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
