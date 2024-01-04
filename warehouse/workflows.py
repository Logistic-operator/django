from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from .activities import drawAllIsos, findNearestStation, create
from .activities import ComposeCreateInput



@workflow.defn
class WarehouseIsos:
    @workflow.run
    async def run(self, wh_id) -> str:
        return await workflow.execute_activity(
            drawAllIsos, wh_id, schedule_to_close_timeout=timedelta(seconds=400), retry_policy=RetryPolicy(
                maximum_attempts=2,
                initial_interval=timedelta(seconds=3),
                non_retryable_error_types=["AttributeError", 'IndexError'],
            ),
        )

@workflow.defn
class WarehouseNearest:
    @workflow.run
    async def run(self, wh_id) -> str:
        return await workflow.execute_activity(
            findNearestStation, wh_id, schedule_to_close_timeout=timedelta(seconds=200), retry_policy=RetryPolicy(
                maximum_attempts=2,
                initial_interval=timedelta(seconds=3),
                non_retryable_error_types=["AttributeError", 'IndexError'],
            ),
        )

@workflow.defn
class WarehouseCreate:
    @workflow.run
    async def run(self, input) -> int:

        return await workflow.execute_activity(
            create, input, schedule_to_close_timeout=timedelta(seconds=200), retry_policy=RetryPolicy(
                maximum_attempts=2,
                initial_interval=timedelta(seconds=3),
                non_retryable_error_types=["AttributeError", 'IndexError'],
            ),
        )