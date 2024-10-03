from __future__ import annotations

import logging
import asyncio
import concurrent.futures
import time
from enum import Enum
from typing import Annotated, AsyncGenerator, Any, Callable, Protocol

from annotated_types import MinLen
from pydantic import BaseModel

from shared.data.source import ReadDataSource, WriteDataSource

logger = logging.getLogger(__name__)


class Handler(Protocol):
    async def handle(self, message: Any) -> bool:
        ...


class Consumer(BaseModel):
    name: str | Enum
    reader_factory: Callable[[], ReadDataSource]
    handler_factory: Callable[[], Handler]
    dlq_factory: Callable[[], WriteDataSource] | None = None
    criteria: Any = None    # TODO move into Reader
    timeout: float | None = None
    workers: int = 1


class Pool:
    def __init__(self) -> None:
        pass

    def debug(self, consumer: Consumer) -> None:
        asyncio.run(self._consume(f"{consumer.name}:debug", consumer, stop_on_error=True))

    def consume(
            self,
            consumers: Annotated[list[Consumer], MinLen(min_length=1)],
            propagate: bool = False
    ) -> None:
        num_workers = sum(consumer.workers for consumer in consumers)
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=num_workers)
        try:
            tasks = [executor.submit(self._run_worker, idx, consumer)
                     for consumer in consumers
                     for idx in range(consumer.workers)]
            for future in concurrent.futures.as_completed(tasks):
                future.result()
        except KeyboardInterrupt as e:
            logger.info("Received Ctrl+C. Shutting down all workers.")
            executor.shutdown(wait=True)
            if propagate:
                raise e
        logger.info('DONE')

    async def _consume(self, idx: str, consumer: Consumer, stop_on_error: bool = False) -> None:
        logger.info(f"Consumer #{idx} is consuming...")
        handler = consumer.handler_factory()
        reader = consumer.reader_factory().get_reader()
        dlq = consumer.dlq_factory().get_writer() if consumer.dlq_factory else None

        async for message in reader.filter(consumer.criteria).read():
            start_time = time.time()
            logger.info(f"Consumer #{idx} received message: {message}")
            try:
                result = await handler.handle(message)
                if not result:
                    raise RuntimeError('no result')
            except Exception as e:
                logger.error(f'Consumer #{idx}: Task failed with error: {e}', exc_info=True, stack_info=True)
                if stop_on_error:
                    await reader.close()
                    raise e
                if dlq:
                    logger.info(f'Consumer #{idx}: Redirecting message to DLQ')
                    await dlq.write(message, str(e))

            end_time = time.time()
            logger.info(f"Consumer #{idx} processed message in {end_time - start_time:.2f} seconds")

        await reader.close()

    async def _consume_with_timeout(self, idx: str, consumer: Consumer, timeout: float) -> None:
        """
        Consumer restarts periodically to refresh its metadata cache
        """
        try:
            await asyncio.wait_for(self._consume(idx, consumer), timeout)
        except asyncio.TimeoutError:
            logger.warning(f"Consumer #{idx} timed out")

    def _run_worker(self, pool: int, consumer: Consumer) -> None:
        idx = f'{consumer.name}:{pool}'
        logger.info(f'Run Consumer Worker #{idx}')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            while True:
                try:
                    if consumer.timeout:
                        loop.run_until_complete(self._consume_with_timeout(idx, consumer, consumer.timeout))
                    else:
                        loop.run_until_complete(self._consume(idx, consumer))
                    logger.info(f"Consumer #{idx} exited normally. Restarting...")
                except Exception as e:
                    logger.error(f"Consumer #{idx} exited with error {e}. Retrying...")
                    time.sleep(1)
        finally:
            loop.close()
