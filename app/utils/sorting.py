from sqlalchemy import asc, desc


def sort_direction_to_func():
    return {
        "asc": asc,
        "desc": desc,
    }


def sort_encapsulate_query(
        sort_by: str,
        sort_direction: str,
        sort_attr_to_col: dict,
        query
):
    if sort_by is None:
        return query

    sort_dir_mapping = sort_direction_to_func()
    sort_by_col = sort_attr_to_col.get(sort_by, None)
    sort_dir_func = sort_dir_mapping.get(sort_direction, None)

    if sort_by_col is None or sort_dir_func is None:
        raise Exception("sort_by provided but sort_by and/or sort_dir invalid")

    return query.order_by(sort_dir_func(sort_by_col))
