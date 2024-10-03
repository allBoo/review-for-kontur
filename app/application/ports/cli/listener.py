from __future__ import annotations

import logging
from functools import partial

import typer
from enum import Enum
from typing import Annotated, Optional
from annotated_types import Ge, MinLen

from application.service.factory import ServiceFactory
from events.service.router import PingRoute, AdPlaysRoute, ContentPlaysRoute
from shared.infrastructure.queue.consumer import Consumer, Pool

logger = logging.getLogger(__name__)

__all__ = ['register']


class ConsumerType(Enum):
    ROUTER = "router"
    PING = "ping"
    AD_PLAY = "ads"
    CONTENT_PLAY = "content"


def consumer(
        workers: Annotated[
            Optional[int],
            Ge(ge=1),
            typer.Option(
                ..., "--workers", "-w",
                help="Amount of processes to run for each consumer."
            )] = None,
        consumer_types: Annotated[
            Optional[list[ConsumerType]],
            MinLen(min_length=1),
            typer.Option(
                ..., "--consumer-types", "-t",
                help="Consumer types to run."
            )] = None,
        debug: Annotated[bool, typer.Option(help="Run in a single thread with no retries")] = False,
        consumer_group: Annotated[
            Optional[str],
            typer.Option(
                ..., "--consumer-group", "-g",
                help="Consumer group name"
            )] = None
) -> None:
    consumers = [
        Consumer(
            name=ConsumerType.ROUTER,
            reader_factory=partial(ServiceFactory.get_events_data_source, consumer_group),  # <- do not use lambdas
            handler_factory=ServiceFactory.get_events_router,
            workers=1,
        ),
        Consumer(
            name=ConsumerType.PING,
            reader_factory=partial(ServiceFactory.get_events_data_source, consumer_group),
            criteria=[PingRoute],
            handler_factory=ServiceFactory.get_ping_event_handler,
            dlq_factory=partial(ServiceFactory.get_dlq_writer),
            timeout=3600.0,
            workers=2,
        ),
        Consumer(
            name=ConsumerType.AD_PLAY,
            reader_factory=partial(ServiceFactory.get_events_data_source, consumer_group),
            criteria=[AdPlaysRoute],
            handler_factory=ServiceFactory.get_ad_event_handler,
            dlq_factory=partial(ServiceFactory.get_dlq_writer),
            timeout=3600.0,
            workers=2,
        ),
        Consumer(
            name=ConsumerType.CONTENT_PLAY,
            reader_factory=partial(ServiceFactory.get_events_data_source, consumer_group),
            criteria=[ContentPlaysRoute],
            handler_factory=ServiceFactory.get_content_event_handler,
            dlq_factory=partial(ServiceFactory.get_dlq_writer),
            timeout=3600.0,
            workers=2,
        ),
    ]

    if consumer_types is not None:
        consumers = [c for c in consumers if c.name in consumer_types]

    cpool = Pool()
    if debug:
        logging.root.setLevel(logging.DEBUG)
        logger.info(f'Run Consumer {consumers[0].name} in a single thread')
        cpool.debug(consumers[0])
    else:
        if workers:
            for consumer in consumers:
                consumer.workers = workers
            logger.info(f'Run Consumers {[c.name for c in consumers]} with {workers} workers for each')
        else:
            logger.info(f'Run Consumers {[c.name for c in consumers]}')
        cpool.consume(consumers)


def register(app: typer.Typer) -> None:
    app.command(name="listen")(consumer)
