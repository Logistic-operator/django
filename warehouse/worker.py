from warehouse.activities import drawAllIsos, findNearestStation, create
from warehouse.workflows import WarehouseIsos, WarehouseNearest, WarehouseCreate
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client, task_queue="wh-task-queue", 
        workflows=[WarehouseIsos, WarehouseNearest, WarehouseCreate], 
        activities=[drawAllIsos, findNearestStation, create]
    )
    await worker.run()