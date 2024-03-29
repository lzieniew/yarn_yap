import asyncio


def run_async(async_func):
    """
    Utility function that runs an async function using the current event loop
    """
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # In case the loop is already running use asyncio.ensure_future
        return asyncio.ensure_future(async_func)
    else:
        return loop.run_until_complete(async_func)

