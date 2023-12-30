# @@@SNIPSTART python-project-template-run-workflow
import asyncio

from run_worker import WarehouseNearest, WarehouseIsos, RailwayOptimize
from temporalio.client import Client


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")
    # await client.execute_workflow(
    #     WarehouseIsos.run, 29, id="wh-workflow1", task_queue="wh-task-queue"
    # )

    # Execute a workflow
    result = await client.execute_workflow(
        RailwayOptimize.run, id="rw-workflow", task_queue="wh-task-queue"
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND
