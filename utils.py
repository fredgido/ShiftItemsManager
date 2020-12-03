import datetime
from sqlalchemy import inspect


def serialize(query_result, fields=(), exclude=()):
    if not query_result:
        return ()
    if not isinstance(query_result, list):
        query_result = [query_result]
    attrs = set([attr.key for attr in inspect(query_result[0]).mapper.column_attrs])
    attrs = attrs - set(exclude)
    if fields:
        attrs = attrs.intersection(set(fields))

    result_list = []
    for obj in query_result:
        dic = {}
        for attr in attrs:
            dic[attr] = getattr(obj, attr, None)
            if isinstance(dic[attr], datetime.datetime):
                dic[attr] = dic[attr].isoformat()
        result_list.append(dic)
    return result_list
