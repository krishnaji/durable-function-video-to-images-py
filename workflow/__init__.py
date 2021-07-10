# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    logging.info("EVGInputs------------->%s",context._input)
    sasLink = yield context.call_activity('Task_GetSasUri', context._input)
    logging.info("sasLinkAF------------->%s",sasLink)
    downLoadFile = yield context.call_activity('Task_DownloadBlob',sasLink)
    logging.info("downloadAF------------->%s",downLoadFile)
    vidToImages = yield context.call_activity('Task_VidToImage',downLoadFile)

    
    return [downLoadFile]

main = df.Orchestrator.create(orchestrator_function)