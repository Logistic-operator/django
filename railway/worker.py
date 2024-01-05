from railway.activities import create, createNb, optimize
from railway.workflows import RailwayCreate, RailwayCreateNb, RailwayOptimize
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client, task_queue="rw-task-queue", 
        workflows=[RailwayCreate, RailwayCreateNb, RailwayOptimize], 
        activities=[create, createNb, optimize]
    )
    await worker.run()