import asyncio

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from activities import findNearestRailway, drawAllIsos, optimize
from workflows import WarehouseNearest, WarehouseIsos, RailwayOptimize

async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client, task_queue="wh-task-queue", workflows=[WarehouseNearest, WarehouseIsos, RailwayOptimize], activities=[findNearestRailway, drawAllIsos, optimize]
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())