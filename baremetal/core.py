from __future__ import annotations

import abc
import asyncio
from typing import Any, Iterable, TypeVar, Generic

from baremetal import asyncable
from baremetal.exceptions import ProxyUnavailableException

T = TypeVar("T")

U = TypeVar("U")


class Proxy(Generic[T, U], abc.ABC):
    def __init__(self):
        self.coordinator = Coordinator(proxy=self)

    @abc.abstractmethod
    def batch_inference(self, arguments: Iterable[Any]) -> Any:
        pass

    async def inference(self, argument: T) -> U:
        return await self.coordinator.inference(argument)


class Engine:

    def __init__(self, scheduler: Scheduler, proxy: Proxy = None):
        self.scheduler = scheduler
        self._proxy = proxy

    def set_proxy(self, proxy: Proxy):
        self._proxy = proxy

    async def run(self):
        while True:
            batch = await self.scheduler.join()

            if not self._proxy:
                raise ProxyUnavailableException(
                    "No proxy available, Please set a proxy first."
                )

            if not batch:
                continue

            futures, arguments = list(zip(*batch))

            results = await asyncable.run_in_executor(
                executor_or_config=None,
                func=self._proxy.batch_inference,
                arguments=arguments,
            )
            for future, result in zip(futures, results):
                future.set_result(result)


class Scheduler:

    def __init__(self, batch_size: int = 64):
        if batch_size < 1:
            raise ValueError("Not allowed batch size under 1.")

        self.batch_size = batch_size
        self.queue = asyncio.Queue()

    def schedule(self, future: asyncio.Future, argument: Any):
        self.queue.put_nowait((future, argument))

    async def join(self) -> list[tuple[asyncio.Future, Any]]:
        argument = await self.queue.get()
        batch = [argument]
        for _ in range(self.batch_size - 1):
            if self.queue.empty():
                break
            args = self.queue.get_nowait()
            batch.append(args)
        return batch


class Coordinator:

    def __init__(self, proxy: Proxy = None):
        self.scheduler = Scheduler()
        self.engine = Engine(scheduler=self.scheduler, proxy=proxy)
        self.engine_task = asyncio.create_task(self.engine.run())

    def set_proxy(self, proxy: Proxy):
        self.engine.set_proxy(proxy)

    def inference(self, argument: Any) -> asyncio.Future:
        future = asyncio.Future()
        self.scheduler.schedule(future, argument)
        return future
