import dagster as dg


# assets for job_1
@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_1():
    return [1]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_2():
    return [2]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_3():
    return [3]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_4():
    return [4]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_5():
    return [5]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_6():
    return [6]


# assets for job_2
@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_7():
    return [1]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_8(asset_7):
    return asset_7 + [2]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_9(asset_8):
    return asset_8 + [3]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_10(asset_9):
    return asset_9 + [4]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_11(asset_10):
    return asset_10 + [5]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_12(asset_11):
    return asset_11+ [6]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_13(asset_12):
    return asset_12 + [7]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_14(asset_13):
    return asset_13 + [8]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_15(asset_14):
    return asset_14 + [9]

@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_16(asset_15):
    return asset_15+ [10]


# assets for job_3
@dg.asset(group_name="sor_1",
          tags={"consumer_2":"",
                "consumer_4":""})
def asset_17():
    return [1]