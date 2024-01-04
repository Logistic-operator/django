from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from .activities import create, createNb
from .activities import ComposeCreateInput

@workflow.defn
class RailwayCreate:
    @workflow.run
    async def run(self, input) -> int:

        return await workflow.execute_activity(
            create, input, schedule_to_close_timeout=timedelta(seconds=200), retry_policy=RetryPolicy(
                maximum_attempts=2,
                initial_interval=timedelta(seconds=3),
                non_retryable_error_types=["AttributeError", 'IndexError'],
            ),
        )

@workflow.defn
class RailwayCreateNb:
    @workflow.run
    async def run(self, input) -> int:

        return await workflow.execute_activity(
            createNb, input, schedule_to_close_timeout=timedelta(seconds=200), retry_policy=RetryPolicy(
                maximum_attempts=2,
                initial_interval=timedelta(seconds=3),
                non_retryable_error_types=["AttributeError", 'IndexError'],
            ),
        )