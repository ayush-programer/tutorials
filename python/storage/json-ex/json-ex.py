# Python3 JSON Examples

import json

from captain import Captain
from starships import Starship, KlingonStarship

starship_list = [
        Starship("Enterprise", Captain(name="Jean-Luc", surname="Picard")),
        Starship("Voyager", Captain(name="Kathryn", surname="Janeway")),
        Starship("Defiant", Captain(name="Benjamin", surname="Sisco")),
        Starship("Unknown", Captain(name="Nobody"))
        ]

json_data = json.dumps(starship_list, default=lambda o: o.__dict__, indent=4)

with open("starships.json", "w") as json_file:
    json.dump(json_data, json_file)

with open("starships.json") as json_file:
    json_data_reloaded = json.load(json_file)

print(json_data_reloaded)
# [
#     {
#         "name": "Enterprise",
#         "captain": {
#             "name": "Jean-Luc",
#             "surname": "Picard"
#         },
#         "stardate": 0
#     },
#     {
#         "name": "Voyager",
#         "captain": {
#             "name": "Kathryn",
#             "surname": "Janeway"
#         },
#         "stardate": 0
#     },
#     {
#         "name": "Defiant",
#         "captain": {
#             "name": "Benjamin",
#             "surname": "Sisco"
#         },
#         "stardate": 0
#     },
#     {
#         "name": "Unknown",
#         "captain": {
#             "name": "Nobody"
#         },
#         "stardate": 0
#     }
# ]
starship_list_reloaded = []

for starship in json.loads(json_data_reloaded):

    starship_list_reloaded.append(

        Starship(
            starship["name"],
            Captain(
                starship["captain"]["name"],
                starship["captain"]["surname"]
                    if "surname" in starship["captain"].keys()
                    else ""
                )
            )
        )

print("Starship list:")
for starship in starship_list_reloaded:
    print(
            "\t* {}\t{}".format(starship.name, starship.captain.get_name())
        )
# Starship list:
# 	* Enterprise	(captain: Jean-Luc Picard)
# 	* Voyager	(captain: Kathryn Janeway)
# 	* Defiant	(captain: Benjamin Sisco)
# 	* Unknown	(captain: Nobody)

