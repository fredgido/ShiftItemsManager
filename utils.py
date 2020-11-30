import json
import datetime
from json import JSONEncoder
from sqlalchemy import inspect


def serialize(query_result, fields=(), exclude=()):
    attrs = [attr.key for attr in inspect(query_result[0]).mapper.column_attrs]
    list = []
    for obj in query_result:
        dic = {}
        for attr in attrs:
            dic[attr] = getattr(obj, attr, None)
            if isinstance(dic[attr], datetime.datetime):
                dic[attr] = dic[attr].isoformat()
        list.append(dic)
    return list

# class CustomEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.isoformat()
#         if isinstance(obj, dict):
#             return obj
#         try:
#             JSONEncoder.default(self, obj)
#         except:
#             obj = obj.__dict__.copy()
#             obj.pop('_sa_instance_state')
#         return self.default(obj)
#         #json.dumps(obj, cls=JsonEncoder)
#
#
# def serialize(query, fields=()):
#     return json.loads(json.dumps(query, cls=CustomEncoder))
