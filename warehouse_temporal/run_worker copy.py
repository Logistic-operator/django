import asyncio

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from warehouse_temporal.activities import drawAllIsos
from warehouse_temporal.workflows import WarehouseIsos

async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client, task_queue="wh-task-queue", workflows=[WarehouseNearest, WarehouseIsos], activities=[findNearestRailway, drawAllIsos]
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())