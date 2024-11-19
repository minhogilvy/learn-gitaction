import signal
import socket
import sys
import time
import logging
from concurrent import futures
from datetime import datetime
from typing import Dict
from google.cloud.pubsub_v1.futures import Future
from google.cloud.pubsub_v1.subscriber.scheduler import ThreadScheduler

from .client import Subscriber
from .middleware import run_middleware_hook
from .subscription import Callback
from loguru import logger


class PubSub:
    """A Worker manages the subscriptions which consume Google PubSub messages.

    Facilitates the creation of subscriptions if not already created,
    and the starting and stopping the consumption of them.

    :param subscriptions: list :class:`~rdps.subscription.Subscription`
    """

    def __init__(
        self,
        subscriptions,
        client_options,
        gc_project_id=None,
        credentials=None,
        gc_storage_region=None,
        default_ack_deadline=None,
        threads_per_subscription=None,
        default_retry_policy=None,
    ):
        self._subscriber = Subscriber(
            gc_project_id,
            credentials,
            gc_storage_region,
            client_options,
            default_ack_deadline,
            default_retry_policy,
        )
        self._futures: Dict[str, Future] = {}
        self._subscriptions = subscriptions
        self.threads_per_subscription = threads_per_subscription

    def _get_internet_check_endpoint(self, client_options):
        if (
            client_options is not None
            and client_options.get("api_endpoint") is not None
        ):
            return client_options.get("api_endpoint")
        return "www.google.com"

    def setup(self):
        """Create the subscriptions on a Google PubSub topic.

        If the subscription already exists, the subscription will not be
        re-created. Therefore, it is idempotent.
        """
        logger.debug(f"[start] start setup")
        for subscription in self._subscriptions:
            self._subscriber.update_or_create_subscription(subscription)
        logger.debug(f"[setup] end setup")

def create_and_run(subs, config):
    """
    Create and run a worker from a list of Subscription objects and a config
    while waiting forever, until the process is stopped.

    We stop a worker process on:
    - SIGINT
    - SIGTSTP

    :param subs: List :class:`~rdps.subscription.Subscription`
    :param config: :class:`~rdps.config.Config`
    """
    logger.debug(f"" f"Configuring worker with {len(subs)} subscription(s)...")
    client = PubSub(
        subs,
        config.client_options,
        config.gc_project_id,
        config.credentials,
        config.gc_storage_region,
        config.ack_deadline,
        config.threads_per_subscription,
        config.retry_policy,
    )
    client.setup()