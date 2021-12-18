from uk_covid19 import Cov19API


all_nations = [
    "areaType=nation"
]

cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeathsByDeathDate": "newDeathsByDeathDate",
    "cumDeathsByDeathDate": "cumDeathsByDeathDate"
}

api = Cov19API(
    filters=all_nations,
    structure=cases_and_deaths,
    latest_by="newCasesByPublishDate"
)

json_data = api.get_json(as_string=True)
print("JSON:", json_data)

xml_data = api.get_xml(as_string=True)
print("XML:", xml_data)
