from collections import defaultdict
from fastapi import FastAPI
from typing import Tuple, Dict, List, Any
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRoute
from .handlers import register_error_handling
from .health import router
from ..config import get_settings
from .version import version_to_route

def get_application() -> FastAPI:
    # Main Fast API application
    setttings = get_settings()
    app = FastAPI(
        openapi_url=f"/openapi.json",
        **setttings.col_kwargs
    )
    
    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Set Up the static files and directory to serve django static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    register_error_handling(app)
    return app


def get_application_with_version(
    app: FastAPI,
    version_format: str = "{major}",
    prefix_format: str = "/v{major}",
    default_version: Tuple[int, int] = (1,0),
    enable_latest: bool = False
) -> FastAPI:
    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    version_route_mapping: Dict[Tuple[int, int], List[APIRoute]] = defaultdict(
        list
    )
    version_routes = [
        version_to_route(route, default_version) for route in app.routes
    ]

    for version, route in version_routes:
        version_route_mapping[version].append(route)

    unique_routes = {}
    versions = sorted(version_route_mapping.keys())
    for version in versions:
        major, minor = version
        prefix = prefix_format.format(major=major)
        semver = version_format.format(major=major)
        version_app = FastAPI(
            title=app.title,
            description=app.description,
            version=semver,
        )
        for route in version_route_mapping[version]:
            for method in route.methods:
                unique_routes[route.path + "|" + method] = route
        for route in unique_routes.values():
            version_app.router.routes.append(route)
        app.mount(prefix, version_app)

        @app.get(
            f"{prefix}/openapi.json", name=semver, tags=["Versions"]
        )

        @app.get(f"{prefix}/docs", name=semver, tags=["Documentations"])
        def noop() -> None:
            pass

    if enable_latest:
        prefix = "/latest"
        major, minor = version
        semver = version_format.format(major=major, minor=minor)
        version_app = FastAPI(
            title=app.title,
            description=app.description,
            version=semver,
        )
        for route in unique_routes.values():
            version_app.router.routes.append(route)
        app.mount(prefix, version_app)

    # Set Up the static files and directory to serve django static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(router)
    register_error_handling(app)
    return app
