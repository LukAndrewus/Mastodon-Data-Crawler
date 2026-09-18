
# testlist = [
#     {"id": 1234},
#     {"id": 4567},
#     {"id": 1234},
# ]

# seen = set()
# for dict in testlist:
#     if dict["id"] in seen:
#         testlist.remove(dict)
#     else:
#         seen.add(dict["id"])

# print(testlist)
import datetime

x = datetime.datetime.now()

print(x.date())