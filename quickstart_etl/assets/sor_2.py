import dagster as dg


# assets for job_1
@dg.asset(group_name="sor_2",
          tags={"consumer_1":"",
                "consumer_2":"",
                "consumer_3":"",
                "consumer_5":""})
def asset_18():
    return [1]

# assets for job_2

@dg.asset(group_name="sor_2",
          tags={"consumer_1":"",
                "consumer_2":"",
                "consumer_3":"",
                "consumer_5":""})
def asset_19():
    return [2]

# assets for job_3

@dg.asset(group_name="sor_2",
          tags={"consumer_1":"",
                "consumer_2":"",
                "consumer_3":"",
                "consumer_5":""},
          deps=[asset_18])
def asset_20():
    return [3]

# assets for 4

@dg.asset(group_name="sor_2",
          tags={"consumer_1":"",
                "consumer_2":"",
                "consumer_3":"",
                "consumer_5":""},
          deps=[asset_19, asset_20])
def asset_21():
    return [4]