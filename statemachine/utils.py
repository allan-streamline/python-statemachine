import threading

from anyio.from_thread import BlockingPortalProvider

_cached_portal = threading.local()
_cached_portal.provider = BlockingPortalProvider()
"""Loop that will be used when the SM is running in a synchronous context. One loop per thread."""


def qualname(cls):
    """
    Returns a fully qualified name of the class, to avoid name collisions.
    """
    return ".".join([cls.__module__, cls.__name__])


def ensure_iterable(obj):
    """
    Returns an iterator if obj is not an instance of string or if it
    encounters type error, otherwise it returns a list.
    """
    if isinstance(obj, str):
        return [obj]
    try:
        return iter(obj)
    except TypeError:
        return [obj]


async def _do(coroutine):
    return await coroutine


def run_async_from_sync(coroutine):
    """
    Compatibility layer to run an async coroutine from a synchronous context.
    """
    global _cached_portal
    with _cached_portal.provider as portal:
        return portal.call(_do, coroutine)
