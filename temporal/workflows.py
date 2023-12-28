from datetime import timedelta
from temporalio import workflow

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import createWH

@workflow.defn
class SayHello:
    @workflow.run
    async def run(self, newWH) -> str:
        return await workflow.execute_activity(
            createWH, newWH, start_to_close_timeout=timedelta(seconds=10)
        )