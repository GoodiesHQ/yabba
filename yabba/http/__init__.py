from asyncio_pool import AioPool
from asyncio_pool.results import getres
from yabba.utils import C, target_tasks
import aiohttp
import sys


async def brute_basic(http_target_factory,
                      combo_factory = None,
                      username_factory = None,
                      password_factory = None,
                      pool_size: int = 100,
                      timeout: float = 5.0,
                      output: str = None,
                      verbose: bool = False):
    tasks = target_tasks(http_target_factory, combo_factory, username_factory, password_factory)

    async with AioPool(pool_size) as pool:
        suc_files = [sys.stdout]
        err_files = [sys.stderr]

        if output:
            f = open(output, "w")
            suc_files.append(f)


        async for (val, err) in pool.itermap(worker, tasks, timeout=timeout, get_result=getres.pair):
            #TODO do it
            pass
