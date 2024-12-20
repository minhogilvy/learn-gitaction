from typing import Any, Type
from fastapi.routing import APIRoute

def version_api_route(
    major: int = 1, 
    minor: int = 0, 
    route_class: Type[APIRoute] = APIRoute
) -> Type[APIRoute]:
    class VersionAPIRoute(route_class):  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            try:
                self.endpoint._api_version = (major, minor)
            except AttributeError:
                self.endpoint.__func__._api_version = (major, minor)

    return VersionAPIRoute
