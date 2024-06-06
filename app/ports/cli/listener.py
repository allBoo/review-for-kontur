import logging
from typing import Annotated
from annotated_types import Ge

import typer
import asyncio
import concurrent.futures
import time

from app.service.factory import ServiceFactory
from app.data.models.raw_events import EventType

__all__ = ['register']

logger = logging.getLogger(__name__)


async def listen(idx: str, event_type: EventType) -> None:
    logger.info(f"Listener #{idx} is listening...")
    service = ServiceFactory.get_raw_events_primary_reader()
    async for event in service.read_from([event_type.value]).read():
        logger.info(f"Listener #{idx} received event: {event}")


async def listen_with_timeout(idx: str, event_type: EventType, timeout: int) -> None:
    """
    Listener restarts periodically to refresh its metadata cache
    :param idx:
    :param event_type:
    :param timeout:
    :return:
    """
    try:
        await asyncio.wait_for(listen(idx, event_type), timeout)
    except asyncio.TimeoutError:
        logger.warning(f"Listener #{idx} timed out")


def listener_async_manager(idx: str, event_type: EventType) -> None:
    logger.info(f"Started Listener #{idx}...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        while True:
            try:
                loop.run_until_complete(listen_with_timeout(idx, event_type, 2))
                logger.info(f"Listener #{idx} exited normally. Restarting...")
            except Exception as e:
                logger.warning(f"Listener #{idx} exited with error: {e}. Retrying...")
                time.sleep(1)
    finally:
        loop.close()


def run_pool(pool: int, event_types: list[EventType]) -> None:
    logger.info(f'Run Listener Pool #{pool} for {[e.value for e in event_types]} events')

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(event_types))
    try:
        futures = [executor.submit(listener_async_manager, f'{pool}:{event_type.value}', event_type) for event_type in event_types]
    except KeyboardInterrupt as e:
        logger.info("Received Ctrl+C. Shutting down all listeners.")
        executor.shutdown(wait=True)
        raise e


def listener(
        pools: Annotated[
            int,
            Ge(ge=1),
            typer.Option(help="Amount of processes to run. "
                              "Each process handles every single EventType in a separate thread")] = 1,
        event_types: Annotated[list[EventType], Ge(ge=1)] | None = None,
        debug: Annotated[bool, typer.Option(help="Run in a single thread with no monitoring")] = False
) -> None:
    if event_types is None:
        event_types = [EventType.PING, EventType.PLAY, EventType.ERROR]
    logger.info(f'Run Listener on {pools} pools for {[e.value for e in event_types]} event types each')

    if debug:
        asyncio.run(listen("debug", event_types[0]))
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=pools)
        try:
            futures = [executor.submit(run_pool, idx, event_types) for idx in range(pools)]
        except KeyboardInterrupt as e:
            logger.info("Received Ctrl+C. Shutting down all pools.")
            executor.shutdown(wait=True)
            raise e


def register(app: typer.Typer) -> None:
    app.command(name="listen")(listener)

