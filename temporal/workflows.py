from datetime import timedelta
from temporalio import workflow


# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import findNearestRailway, drawAllIsos, optimize

@workflow.defn
class WarehouseNearest:
    @workflow.run
    async def run(self, wh_id) -> dict:
        return await workflow.execute_activity(
            findNearestRailway, wh_id, start_to_close_timeout=timedelta(seconds=10)
        )

@workflow.defn
class WarehouseIsos:
    @workflow.run
    async def run(self, wh_id) -> dict:
        return await workflow.execute_activity(
            drawAllIsos, wh_id, start_to_close_timeout=timedelta(seconds=10)
        )

@workflow.defn
class RailwayOptimize:
    @workflow.run
    async def run(self) -> str:
        return await workflow.execute_activity(
            optimize, start_to_close_timeout=timedelta(seconds=10)
        )