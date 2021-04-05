import urllib
import json
import time
from azure.storage.blob import *
from azure.storage.blob import BlobServiceClient


def printHttpError(httpError):
    print("The request failed with status code: " + str(httpError.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(httpError.info())

    print(json.loads(httpError.read()))
    return


def saveBlobToFile(blobUrl, resultsLabel):
    output_file = "output.csv"
    print("Reading the result from " + blobUrl)
    try:
        response = urllib.urlopen(blobUrl)
    except urllib.HTTPError as error:
        printHttpError(error)
        return

    with open(output_file, "w+") as f:
        f.write(response.read())
    print(resultsLabel + " have been written to the file " + output_file)
    return


def processResults(result):

    first = True
    results = result["Results"]
    for outputName in results:
        result_blob_location = results[outputName]
        sas_token = result_blob_location["SasBlobToken"]
        base_url = result_blob_location["BaseLocation"]
        relative_url = result_blob_location["RelativeLocation"]

        print(
            "The results for "
            + outputName
            + " are available at the following Azure Storage location:"
        )
        print("BaseLocation: " + base_url)
        print("RelativeLocation: " + relative_url)
        print("SasBlobToken: " + sas_token)

        if first:
            first = False
            url3 = base_url + relative_url + sas_token
            saveBlobToFile(url3, "The results for " + outputName)
    return


def uploadFileToBlob(
    input_file,
    input_blob_name,
    storage_container_name,
    storage_account_name,
    storage_account_key,
):
    blob_service = BlobServiceClient(
        account_name=storage_account_name, account_key=storage_account_key
    )

    print("Uploading the input to blob storage...")
    data_to_upload = open(input_file, "r").read()
    blob_service.put_blob(
        storage_container_name,
        input_blob_name,
        data_to_upload,
        x_ms_blob_type="BlockBlob",
    )


def invokeBatchExecutionService():

    storage_account_name = "saritnewsstore"
    storage_account_key = "xxxxxxxxxxxxxxx"
    storage_container_name = "saritnewscontainer"
    connection_string = (
        "DefaultEndpointsProtocol=https;AccountName="
        + storage_account_name
        + ";AccountKey="
        + storage_account_key
    )
    api_key = "K7iBX97AH6DisM7ZCvPRBHfEuteQRMfIaNCAicx4XiXDZATNwU0HlB8Bs3TDy9EiMPTD8881V432yFQAw7t6XA=="
    url = "https://ussouthcentral.services.azureml.net/workspaces/7a99451e0feb48d0b0d26bdf368f8527/services/30910a3f69b24797bea2cc2b4bb9f62a/jobs"

    uploadFileToBlob(
        "input1data.csv",
        "input1datablob.csv",
        storage_container_name,
        storage_account_name,
        storage_account_key,
    )

    payload = {
        "Inputs": {
            "input1": {
                "ConnectionString": connection_string,
                "RelativeLocation": "/"
                + storage_container_name
                + "/input1datablob.csv",
            },
        },
        "Outputs": {
            "output1": {
                "ConnectionString": connection_string,
                "RelativeLocation": "/"
                + storage_container_name
                + "/output1results.csv",
            },
        },
        "GlobalParameters": {},
    }

    body = str.encode(json.dumps(payload))
    headers = {
        "Content-Type": "application/json",
        "Authorization": ("Bearer " + api_key),
    }
    print("Submitting the job...")

    # submit the job
    req = urllib.Request(url + "?api-version=2.0", body, headers)
    try:
        response = urllib.urlopen(req)
    except urllib.HTTPError as error:
        printHttpError(error)
        return

    result = response.read()
    job_id = result[1:-1]
    print("Job ID: " + job_id)

    # start the job
    print("Starting the job...")
    req = urllib.Request(url + "/" + job_id + "/start?api-version=2.0", "", headers)
    try:
        response = urllib.urlopen(req)
    except urllib.HTTPError as error:
        printHttpError(error)
        return

    url2 = url + "/" + job_id + "?api-version=2.0"

    while True:
        print("Checking the job status...")

        req = urllib.Request(url2, headers={"Authorization": ("Bearer " + api_key)})

        try:
            response = urllib.urlopen(req)
        except urllib.HTTPError as error:
            printHttpError(error)
            return

        result = json.loads(response.read())
        status = result["StatusCode"]
        if status == 0 or status == "NotStarted":
            print("Job " + job_id + " not yet started...")
        elif status == 1 or status == "Running":
            print("Job " + job_id + " running...")
        elif status == 2 or status == "Failed":
            print("Job " + job_id + " failed!")
            print("Error details: " + result["Details"])
            break
        elif status == 3 or status == "Cancelled":
            print("Job " + job_id + " cancelled!")
            break
        elif status == 4 or status == "Finished":
            print("Job " + job_id + " finished!")

            processResults(result)
            break
        time.sleep(1)  # wait one second
    return


invokeBatchExecutionService()