from typing import Any, Callable, TypeVar, Tuple, cast
from fastapi.routing import APIRoute
from starlette.routing import BaseRoute

CallableT = TypeVar("CallableT", bound=Callable[..., Any])
def version(
    major: int, 
    minor: int = 0
) -> Callable[[CallableT], CallableT]:
    def decorator(func: CallableT) -> CallableT:
        func._api_version = (major, minor)  # type: ignore
        return func

    return decorator

def version_to_route(
    route: BaseRoute,
    default_version: Tuple[int, int]
) -> Tuple[Tuple[int, int], APIRoute]:
    route_ = cast(APIRoute, route)
    version = getattr(
        route_.endpoint, 
        "_api_version", 
        default_version
    )
    return version, route_