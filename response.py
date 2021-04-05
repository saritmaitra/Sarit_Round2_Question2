import urllib.request
import json
import urllib
from urllib.error import HTTPError


data = {
    "Inputs": {
        "input1": {
            "ColumnNames": ["date_of_news", "title", "hyperlink", "Key Phrases"],
            "Values": [
                ["value", "value", "value", "value"],
                ["value", "value", "value", "value"],
            ],
        },
    },
    "GlobalParameters": {},
}

body = str.encode(json.dumps(data))

url = "https://ussouthcentral.services.azureml.net/workspaces/7a99451e0feb48d0b0d26bdf368f8527/services/30910a3f69b24797bea2cc2b4bb9f62a/execute?api-version=2.0&details=true"
api_key = "K7iBX97AH6DisM7ZCvPRBHfEuteQRMfIaNCAicx4XiXDZATNwU0HlB8Bs3TDy9EiMPTD8881V432yFQAw7t6XA=="
headers = {"Content-Type": "application/json", "Authorization": ("Bearer " + api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)
    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))
