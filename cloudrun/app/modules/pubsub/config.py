import importlib
import os

from google.oauth2 import service_account

from .client import (
    DEFAULT_ACK_DEADLINE,
    DEFAULT_BLOCKING,
    DEFAULT_ENCODER_PATH,
    get_google_defaults,
)
from .middleware import register_middleware
from .publishing import init_global_publisher
from .subscription import Subscription
from app.config import GOOGLE_APPLICATION_CREDENTIALS
from dotenv import load_dotenv
load_dotenv()

class Config:
    _instance = None
    """Configuration class.

    The settings dictionary will be parsed into an easily
    accessible object containing all the necessary constants.

    If no middleware is set, the *default_middleware* will be added.

    :param setting: dict :ref:`settings <_settings>`
    """

    def __init__(self):

        self._gc_project_id = os.environ.get("GC_PROJECT_ID", "cp-gcp-prod-osbotogilvy")
        self.gc_credentials_path = GOOGLE_APPLICATION_CREDENTIALS
        
        self.gc_storage_region = os.environ.get("GC_STORAGE_REGION", "asia-southeast1")
        self.app_name = os.environ.get("APP_NAME")
        self.sub_prefix = os.environ.get("SUB_PREFIX")
        self.middleware = os.environ.get("MIDDLEWARE", ['app.modules.pubsub.contrib.LoggingMiddleware'])
        self.ack_deadline = os.environ.get(
            "ACK_DEADLINE",
            os.environ.get("DEFAULT_ACK_DEADLINE", DEFAULT_ACK_DEADLINE),
        )
        self.publisher_blocking = os.environ.get("PUBLISHER_BLOCKING", DEFAULT_BLOCKING)
        self._encoder_path = os.environ.get("ENCODER_PATH", DEFAULT_ENCODER_PATH)
        self.publisher_timeout = os.environ.get("PUBLISHER_TIMEOUT", 3.0)
        self.threads_per_subscription = os.environ.get("THREADS_PER_SUBSCRIPTION", 5)
        self.filter_by = os.environ.get("FILTER_SUBS_BY")
        self._credentials = None
        self.retry_policy = os.environ.get("DEFAULT_RETRY_POLICY")
        self.client_options = os.environ.get("CLIENT_OPTIONS")
    
    def __new__(cls):
        """
        Create a new instance of the class if it doesn't 
        exist, otherwise return the existing instance.

        Returns:
            TranslationWrapper: The instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def encoder(self):
        module_name, class_name = self._encoder_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    @property
    def credentials(self):
        if self.gc_credentials_path:
            try:
                self._credentials = service_account.Credentials.from_service_account_file(
                    self.gc_credentials_path
                )
            except Exception as ex:
                print(f"Error: {ex}")
        else:
            credentials, project_id = get_google_defaults()
            self._credentials = credentials
            if not self._gc_project_id:
                self._gc_project_id = project_id
        return self._credentials

    @property
    def gc_project_id(self):
        if self._gc_project_id:
            return self._gc_project_id
        elif self.credentials:
            return self.credentials.project_id
        else:
            return None


def setup(setting=None, **kwargs):
    if setting is None:
        setting = {}

    config = Config()
    init_global_publisher(config)
    register_middleware(config, **kwargs)
    return config


def is_same_subscription(a_subscription, another_subscription):
    return id(a_subscription) == id(another_subscription)


def is_subscription_registered(subscriptions, current_subscription):
    registered_subscription = subscriptions.get(current_subscription.name)
    return is_same_subscription(registered_subscription, current_subscription)


def subscription_from_attribute(attribute):
    try:
        if isinstance(attribute, Subscription):
            subscription = attribute
        elif issubclass(attribute, Subscription):
            subscription = attribute()
        else:
            return None
    except TypeError:
        # If attribute is not a class, TypeError is raised when testing issubclass
        return None
    return subscription


def load_subscriptions_from_paths(sub_module_paths, sub_prefix=None, filter_by=None):
    subscriptions = {}
    
    for sub_module_path in sub_module_paths:
        sub_module = importlib.import_module(sub_module_path)
        for attr_name in dir(sub_module):
            attribute = getattr(sub_module, attr_name)

            subscription = subscription_from_attribute(attribute)
            if not subscription:
                continue

            if sub_prefix and not subscription.prefix:
                subscription.set_prefix(sub_prefix)

            if filter_by and not subscription.filter_by:
                subscription.set_filters(filter_by)

            if is_subscription_registered(subscriptions, subscription):
                continue

            if subscription.name in subscriptions:
                found_subscription = subscriptions[subscription.name]
                raise RuntimeError(
                    f"Duplicate subscription name found: {subscription.name}. Subs "
                    f"{subscription._func.__module__}.{subscription._func.__name__} and "
                    f"{found_subscription._func.__module__}.{found_subscription._func.__name__} collide."
                )

            subscriptions[subscription.name] = subscription
    return list(subscriptions.values())
