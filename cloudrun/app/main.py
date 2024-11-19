from fastapi import FastAPI

from .api.app import get_application_with_version
from .api.webhooks import router
from .api.general import general
from .config import get_settings

settings = get_settings()
main_app = FastAPI(
  **settings.col_kwargs
)

main_app.include_router(router)
main_app.include_router(general)
app = get_application_with_version(
  main_app
)