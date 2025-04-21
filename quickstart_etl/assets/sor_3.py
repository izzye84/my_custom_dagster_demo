import dagster as dg


# assets for job_1
@dg.asset(group_name="sor_3")
def asset_22():
    return [1]

# assets for job_2
@dg.asset(group_name="sor_3")
def asset_23():
    return [2]

@dg.asset(group_name="sor_3")
def asset_24(asset_23):
    return asset_23 + [3]

@dg.asset(group_name="sor_3")
def asset_25(asset_24):
    return asset_24 + [4]

@dg.asset(group_name="sor_3")
def asset_26(asset_25):
    return asset_25 + [4]

@dg.asset(group_name="sor_3")
def asset_27(asset_26):
    return asset_26 + [4]