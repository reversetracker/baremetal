from __future__ import annotations

import asyncio
import time

from baremetal import Proxy


class ProxyUnavailableException(Exception):
    pass


class TestProxy(Proxy[str, str]):
    def __init__(self, delay: float = 0.1):
        super().__init__()
        self.delay = delay

    def batch_inference(self, arguments: list[str]) -> list[str]:
        print("토치를 실행 합니다..")
        time.sleep(self.delay)
        print(f"batch progress done: {len(arguments)}")
        print(arguments)
        return list(map(lambda x: f"progressed_{x}", arguments))


async def main():
    delay = 0.1
    # TextProxy 가 우리의 torch 를 이용해서 배치처리 구현 하는 곳.
    test_proxy = TestProxy(delay=delay)

    results = await asyncio.gather(
        *[test_proxy.inference(f"test {i}") for i in range(1000)]
    )
    print(results)

    print("no delay 1 person")
    results = await asyncio.gather(
        *[test_proxy.inference(f"test {i}") for i in range(1)]
    )
    print(results)

    print("no delay 10 person")
    results = await asyncio.gather(
        *[test_proxy.inference(f"test {i}") for i in range(10)]
    )
    print(results)

    print("no delay 10 person")
    results = await asyncio.gather(
        *[test_proxy.inference(f"test {i}") for i in range(10)]
    )
    print(results)

    print("no delay 10 person")
    results = await asyncio.gather(
        *[test_proxy.inference(f"test {i}") for i in range(10)]
    )
    print(results)

    print("다시 접속 폭주")
    results = await asyncio.gather(
        *[test_proxy.inference(f"test {i}") for i in range(1000)]
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
