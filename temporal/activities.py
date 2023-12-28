from temporalio import activity


@activity.defn
async def say_hello(id: int) -> str:
    obj = await Warehouse.objects.afirst()#.aget(id=id)
    res = f"Hello, {obj.phone}!"
    return res