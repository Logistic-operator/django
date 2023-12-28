# @@@SNIPSTART python-project-template-run-workflow
import asyncio

from run_worker import SayHello
from temporalio.client import Client


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    # Execute a workflow
    result = await client.execute_workflow(
        SayHello.run, {
        "phone": "123",
        "point": {
            "type": "Point",
            "coordinates": [
                38.75976563,
                55.42901345
            ]
        }
        }, id="hello-workflow", task_queue="hello-task-queue"
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND
