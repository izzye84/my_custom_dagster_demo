select *
from {{ ref('my_first_model') }}

union all

select *
from {{ ref('my_third_model') }}

union all

select *
from {{ ref('my_fourth_model') }}