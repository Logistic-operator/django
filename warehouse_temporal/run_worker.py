import asyncio

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

import sys
sys.path.append('..')
from warehouse.models import drawAllIsos, WarehouseIsos

async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client, task_queue="wh-task-queue", workflows=[WarehouseIsos], activities=[drawAllIsos]
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())