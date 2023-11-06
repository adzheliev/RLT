"""Validation module receives UI inputs to validate and performs checking"""

from datetime import datetime
import json


def validate(input_string: str) -> dict:
    try:
        output = json.loads(input_string)
    except ValueError:
        error_message = "Введите данные в формате словаря."
        raise ValueError(error_message)
    if "dt_from" not in output:
        error_message = "Отсутствует поле словаря dt_from"
        raise KeyError(error_message)
    if "dt_upto" not in output:
        error_message = "Отсутствует поле словаря dt_upto"
        raise KeyError(error_message)
    if "group_type" not in output:
        error_message = "Отсутствует поле словаря group_type"
        raise KeyError(error_message)
    try:
        dt_from = output.get("dt_from")
        dt_from = datetime.fromisoformat(dt_from)
    except TypeError:
        error_message = \
            'Данные поля dt_from должны быть в формате "2022-09-01T00:00:00"'
        raise TypeError(error_message)
    try:
        dt_upto = output.get("dt_upto")
        dt_upto = datetime.fromisoformat(dt_upto)
    except TypeError:
        error_message = \
            'Данные поля dt_upto должны быть в формате "2022-09-01T00:00:00"'
        raise TypeError(error_message)
    group_type = output.get("group_type")
    if group_type not in ['month', 'day', 'hour']:
        raise ValueError(
            "Поле group_type должно быть 'year', 'month' или 'day'"
        )
    if dt_upto <= dt_from:
        error_message = \
            'Конечная дата не может быть меньше или равной начальной'
        raise ValueError(error_message)
    return output
