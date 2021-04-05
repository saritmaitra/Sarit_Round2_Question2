import urllib
import json
import urllib.request

data = {
    "Inputs": {
        "input1": [
            {
                "date_of_news": "09 September 2020",
                "title": "BASF brings the farm to customers with launch of virtual innovation tour experience",
                "hyperlink": "https://www.basf.com/sg/en/media/news-releases/anz/2020/09/basf-brings-the-farm-to-customers-with-launch-of-virtual-innovat.html",
                "Key Phrases": "tour BASF,BASF Agricultural Solutions,BASF shares,BASF Group,BASF Virtual Innovation website,crop solutions,Agricultural Solutions team,BASF Technical Services Manager,Virtual tour,Agricultural Solutions division,self-guided tour of BASF,BASF generated sales,Virtual Innovation Tour website,Agricultu...",
            }
        ],
    },
    "GlobalParameters": {},
}

body = str.encode(json.dumps(data))

url = "https://ussouthcentral.services.azureml.net/workspaces/7a99451e0feb48d0b0d26bdf368f8527/services/30910a3f69b24797bea2cc2b4bb9f62a/execute?api-version=2.0&format=swagger"
api_key = "K7iBX97AH6DisM7ZCvPRBHfEuteQRMfIaNCAicx4XiXDZATNwU0HlB8Bs3TDy9EiMPTD8881V432yFQAw7t6XA=="
headers = {"Content-Type": "application/json", "Authorization": ("Bearer " + api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read()))
