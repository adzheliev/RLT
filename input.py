"""Module use only for testing purposes"""

import json

# data: dict = {
#     "dt_from": "2022-09-01T00:00:00",
#     "dt_upto": "2022-12-31T23:59:00",
#     "group_type": "month"
# }
#
# data = {
#     "dt_from": "2022-10-01T00:00:00",
#     "dt_upto": "2022-11-30T23:59:00",
#     "group_type": "day"
# }

data: dict = {
    "dt_from": "2022-02-01T00:00:00",
    "dt_upto": "2022-02-02T00:00:00",
    "group_type": "hour"
}


input_data = json.dumps(data)
