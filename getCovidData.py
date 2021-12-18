from uk_covid19 import Cov19API
from influxdb import InfluxDBClient
import json

client = InfluxDBClient(host='192.168.54.30', port=8086)
client.switch_database('covid-19')


# Location filters

filters = [
    ['areaType=nation' , 'areaName=england'],
    ['areaType=utla' , 'areaName=suffolk'],
    ['areaType=utla',  'areaName=essex'],
    ['areaType=ltla', 'areaName=ipswich'],
    ['areaType=utla', 'areaName=hertfordshire']
]

# data structure - collect this data
cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeathsByDeathDate": "newDeathsByDeathDate",
    "cumDeathsByDeathDate": "cumDeathsByDeathDate"
}

def getData(filter, structure):
#    print("getData function - started")
    api = Cov19API(
        filters=filter, 
        structure=structure,
        latest_by="newCasesByPublishDate")
    data=api.get_json()
#    print("getData function - completed")
    return data


'''
j = json.dumps(download)
print(j)
print('----------------------')
extract = download['data']
print(extract)
print (extract[0]['areaName'])
'''


def create_json(data):
    #influx data json structure
    json_body = [
        {
            "measurement": "cases_and_deaths",
            "tags": {
                "areaName": data["data"][0]["areaName"],
                "areaCode": data['data'][0]['areaCode']
            },
            "time": data["lastUpdate"],
            "fields": {
                "newCases": data['data'][0]['newCasesByPublishDate'],
                "cumulativeCases": data['data'][0]['cumCasesByPublishDate'],
                "newDeaths": data['data'][0]['newDeathsByDeathDate'],
                "cumulativeDeaths": data['data'][0]['cumDeathsByDeathDate']
            }
        }
    ]
    return json_body


############################
##       MAIN CODE        ##
############################

if __name__ == "__main__":
    for filter in filters:
        print(filter)
        data = getData(filter, cases_and_deaths)
        print(data)
        print("--------------")
        print(create_json(data))
        print("--------------")
        client.write_points(create_json(data))
        print("Data added for ")
        print(data['data'][0]["areaName"])
 
