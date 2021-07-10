import json
import logging
import azure.durable_functions as df
import azure.functions as func


async def main(event: func.EventGridEvent,starter:str):
    client = df.DurableOrchestrationClient(starter)
    subject = (event.subject).split('/')
    options = {
        "container": subject[4],
        "blob": subject[6]
    }
    logging.info("starter----------------> %s",options)
    instance_id = await client.start_new("workflow", None, options)
    

