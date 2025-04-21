import dagster as dg

from .sor_1 import asset_6, asset_17
from .sor_2 import asset_21
from .sor_3 import asset_22

@dg.asset(group_name="consumer_1",
          tags={"consumer_1":"",
                "consumer_4":""},
          deps=[asset_21, asset_22])
def asset_28():
    return [1, 2, 3]

@dg.asset(group_name="consumer_2",
          tags={"consumer_2":"",
                "consumer_5":""},
          deps=[asset_17, asset_21, asset_22])
def asset_29():
    return [4, 5, 6]

@dg.asset(group_name="consumer_3",
          tags={"consumer_3":""},
          deps=[asset_21])
def asset_30():
    return [7, 8, 9]

@dg.asset(group_name="consumer_4",
          tags={"consumer_4":""},
          deps=[asset_6])
def asset_31():
    return [10, 11, 12]

@dg.asset(group_name="consumer_5",
          tags={"consumer_5":""},
          deps=[asset_29])
def asset_32():
    return [10, 11, 12]
