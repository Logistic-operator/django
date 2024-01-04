from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import findNearestRailway, drawAllIsos

@workflow.defn
class WarehouseNearest:
    @workflow.run
    async def run(self, wh_id) -> dict:
        return await workflow.execute_activity(
            findNearestRailway, wh_id, schedule_to_close_timeout=timedelta(seconds=200), retry_policy=RetryPolicy(
                maximum_attempts=2,
                initial_interval=timedelta(seconds=3),
                non_retryable_error_types=["AttributeError", 'IndexError'],
            ),
        )

@workflow.defn
class WarehouseIsos:
    @workflow.run
    async def run(self, wh_id) -> dict:
        return await workflow.execute_activity(
            drawAllIsos, wh_id, schedule_to_close_timeout=timedelta(seconds=400), retry_policy=RetryPolicy(
                maximum_attempts=2,
                initial_interval=timedelta(seconds=3),
                non_retryable_error_types=["AttributeError", 'IndexError'],
            ),
        )