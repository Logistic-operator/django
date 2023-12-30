# @@@SNIPSTART python-project-template-run-workflow
import asyncio

from run_worker import WarehouseNearest, WarehouseIsos
from temporalio.client import Client


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")
    # await client.execute_workflow(
    #     WarehouseIsos.run, 29, id="wh-workflow1", task_queue="wh-task-queue"
    # )

    # Execute a workflow
    result = await client.execute_workflow(
        WarehouseNearest.run, 29, id="wh-workflow", task_queue="wh-task-queue"
    )

    print(f"Result: {result['nearest_railway_id']}")


if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND
