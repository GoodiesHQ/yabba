from asyncio_pool import AioPool
from yabba.utils import trycast, C
import asyncssh
import sys


async def worker(args):
    host, port, username, password = args
    try:
        auth = dict(username=username, password=password, known_hosts=None)
        (conn, client) = await asyncssh.create_connection(None, host, port, **auth)
    except (asyncssh.Error, ConnectionError, ConnectionResetError, OSError, TimeoutError):
        return None, args
    except Exception as e:
        import traceback
        print(e)
        traceback.print_exc()
        return None, args
    else:
        conn.close()
        return True, args


async def brute(target_factory,
                combo_factory=None,
                username_factory=None,
                password_factory=None,
                pool_size: int = 100,
                timeout: float = 5.0,
                output: str = None,
                verbose: bool = False):
    """
    :param target_factory: function that returns iterable of targets
    :param combo_factory: function that returns iterable of username/password pairs
    :param username_factory: function that returns iterable of usernames
    :param password_factory: function that returns iterable of passwords
    :param pool_size: number of concurrent connections to run
    :param output: output filename
    :param verbose: print failed messages
    :return:
    """
    if combo_factory:
        data = ((*target, *combo)
                for combo in combo_factory()
                for target in target_factory())
    elif username_factory and password_factory:
        data = ((*target, username, password)
                for username in username_factory()
                for password in password_factory()
                for target in target_factory())
    else:
        raise ValueError("Either a combo factory or username/password factory pair must be provided")

    async with AioPool(pool_size) as pool:
        suc_files = [sys.stdout]
        err_files = [sys.stderr]

        if output:
            f = open(output, "w")
            suc_files.append(f)

        from asyncio_pool.results import getres
        async for (val, err) in pool.itermap(worker, data, timeout=timeout, get_result=getres.pair):
            if err:
                print("ERROR")
                print(err)
                continue
            result, (host, port, username, password) = val
            if result is True:
                print(C.GRN, file=sys.stdout, end="")
                for file in suc_files:
                    print("{}@{}:{} {}".format(username, host, port, password), file=file, flush=True)
                print(C.RST, file=sys.stdout, end="")
            elif verbose:
                print(C.RED, file=sys.stderr, end="")
                for file in err_files:
                    print("Failed {}@{}:{} {}".format(username, host, port, password) + C.RST, file=file)
                print(C.RST, file=sys.stderr, end="")

