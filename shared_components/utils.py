import asyncio
from concurrent.futures import ThreadPoolExecutor
import inspect
import logging
import threading
import functools


def run_async(coroutine):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)
