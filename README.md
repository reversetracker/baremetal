# GPU Inference Batch Processing with Asyncio

## Overview

The goal is to handle multiple incoming requests by grouping them into batches and processing each batch efficiently using GPU resources. By using `asyncio`, we can handle asynchronous requests and batch them without blocking the main event loop, optimizing GPU utilization and reducing overhead.

## Benefits

- **Efficiency**: Batch processing reduces the overhead per request, making the use of GPU resources more efficient.
- **Scalability**: The system can handle a large number of concurrent requests, which is critical in high-demand environments.
- **Flexibility**: The batch size and other parameters can be adjusted based on the workload and GPU capacity, allowing for dynamic scaling.

## How to Use

Here's a brief guide on how to use the batch processing system:

1. **Initialize the Components**: Set up the `Proxy`, `Scheduler`, `Engine`, and `Coordinator` components.
2. **Set the Proxy**: Define and set the GPU inference logic in the `Proxy` class.
3. **Schedule Requests**: Use the `Coordinator` to schedule inference requests, which are then handled asynchronously.
4. **Run the Engine**: Start the engine that continuously processes the batches fetched from the `Scheduler`.
5. **Receive Results**: The results of the inference are returned via `asyncio.Future` objects, which resolve once the batch processing is complete.

The implementation effectively allows for handling bursts of requests with minimal delay and maximizes throughput on GPU resources.
