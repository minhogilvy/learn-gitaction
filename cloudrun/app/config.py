import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Tuple, Union, Dict

from pydantic_settings import BaseSettings # type: ignore
from dotenv import load_dotenv
load_dotenv()

ROOT_DIR = Path(__file__).absolute().parent.parent
MODEL_DIR = ''
MODULE_PATHS = os.path.join(ROOT_DIR, 'app/subs')
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(ROOT_DIR, "keys/service-account-colpal.json")
class Settings(BaseSettings):
    debug: bool = False
    title: str = "Colgate Teeth Analysis Classification API"
    version: str = "1.0.0"

    max_file_size: int = 5 * 1024 * 1024  # 5MB
    allowed_content_types: Tuple = ("image/jpeg", "image/png")
    ml_model_dir: str = MODEL_DIR
    num_annotations: int = 5  # Number of top annotations to display

    google_project_id: str = os.environ.get('GOOGLE_PROJECT_ID', 'cp-gcp-prod-osbotogilvy')
    google_location_id: str = os.environ.get('GOOGLE_LOCATION_ID', 'asia-southeast1')
    gemini_model_name: str = os.environ.get('GEMINI_MODEL_NAME', 'gemini-1.5-flash-001')
    pubsub_project_id: Union[str, None] = os.environ.get('PUBSUB_PROJECT_ID', '')

    pubsub_generate_annotations_topic: str = os.environ.get('PUBSUB_TOPIC_ID', 'AI-Colgate-Topic')
    cloud_storage_bucket: str = os.environ.get('CLOUD_STORAGE_BUCKET', 'prod-colgate-dataset-bucket')
    cloud_storage_bucket_obj: str = os.environ.get('CLOUD_STORAGE_BUCKET_OBJECT', 'teethDataset')

    api_endpoint_v1: str = os.environ.get('API_ENDPOINT', "")
    index_endpoint_v1: str = os.environ.get('INDEX_ENDPOINT', "")
    deploy_index_id_v1: str = os.environ.get('DEPLOYED_INDEX_ID', "")
    api_regional_endpoint: str = os.environ.get('API_REGIONAL_ENDPOINT', '')

    firestore_collection: str = os.environ.get('FIRESTORE_COLECTION', 'dataset')
    firestore_reports: str = os.environ.get('FIRESTORE_COLECTION_REPORTS', 'reports')

    api_endpoint_v2: str = os.environ.get('API_ENDPOINT_V2', "")
    index_endpoint_v2: str = os.environ.get('INDEX_ENDPOINT_V2', "")
    deploy_index_id_v2: str = os.environ.get('DEPLOYED_INDEX_ID_V2', "")

    api_endpoint_v3: str = os.environ.get('API_ENDPOINT_V3', "")
    index_endpoint_v3: str = os.environ.get('INDEX_ENDPOINT_V3', "")
    deploy_index_id_v3: str = os.environ.get('DEPLOYED_INDEX_ID_V3', "")

    aes_secret_key: str = os.environ.get('SECRET_KEY', "")
    aes_iv_key: str = os.environ.get('IV_KEY', "")
    whatsapp_secret_token: str = os.environ.get('SECRET_TOKEN', "")


    @property
    def col_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
            "docs_url": None,
            "redoc_url": None
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()