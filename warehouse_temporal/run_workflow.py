import asyncio

from .workflows import WarehouseNearest
from temporalio.client import Client


async def findNearest(id):
    client = await Client.connect("localhost:7233")
    await client.execute_workflow(
        WarehouseNearest.run, id, id="wh-workflow1", task_queue="wh-task-queue"
    )
