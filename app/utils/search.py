from sqlalchemy import not_


def search_encapsulate_query(
        search_by: str,
        search_query: str,
        exclusive: bool,
        search_by_to_col: dict,
        query
):
    if search_by is None or search_query is None or exclusive is None:
        return query

    if search_query.strip() == "":
        return query

    search_by_col = search_by_to_col.get(search_by, None)

    if search_by_col is None:
        raise Exception("Invalid search_by")

    contains_ = search_by_col.contains(search_query)

    return query.filter(not_(contains_) if exclusive else contains_)
