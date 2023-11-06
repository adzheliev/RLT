"""Main logic module receives validated UI inputs and generates output"""

import pymongo
from datetime import datetime


def connection_to_db(token: str, password: str):
    """Function connects to MongoDB using token and password"""

    uri = f"mongodb+srv://{token}:{password}@cluster0.npgcgmv.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri)
    db = client.mongodb
    coll = db.salaries

    return coll


def aggregate_data(dt_from: str, dt_upto: str, group_type: str, coll) -> dict:
    """
    Main aggregation function receives connection
    to DB and generates output
    """

    data_to_group: dict = {
        'month': {'day': 1, 'hour': 0},
        'day': {'day': {"$dayOfMonth": "$dt"}, 'hour': 0},
        'hour': {'day': {"$dayOfMonth": "$dt"}, 'hour': {"$hour": "$dt"}}
    }

    match_cond: dict = {"$match":
                      {"dt":
                           {"$gte": datetime.fromisoformat(dt_from),
                            "$lte": datetime.fromisoformat(dt_upto)
                            }
                       }
                  }

    group_cond: dict = {
                "$group": {
                    "_id": {
                        '$dateFromParts': {
                            'year': {"$year": "$dt"},
                            'month': {"$month": "$dt"},
                            'day': data_to_group[group_type]['day'],
                            'hour': data_to_group[group_type]['hour']
                        }
                    },
                    "total": {"$sum": "$value"}}}

    sort_cond: dict = {"$sort": {"_id": 1}}

    pipeline = coll.aggregate([match_cond, group_cond, sort_cond])

    dataset: list = []
    labels: list = []

    for entry in pipeline:
        dataset.append(entry["total"])
        labels.append(entry['_id'].strftime("%Y-%m-%dT%H:%M:%S"))

    result: dict = {
        "dataset": dataset,
        "labels": labels
    }

    return result
