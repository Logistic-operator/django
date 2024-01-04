from railway.activities import create, createNb
from railway.workflows import RailwayCreate, RailwayCreateNb
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client, task_queue="rw-task-queue", 
        workflows=[RailwayCreate, RailwayCreateNb,], 
        activities=[create, createNb,]
    )
    await worker.run()