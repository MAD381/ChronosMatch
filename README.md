# ChronosMatch — Week 1

## Project
Zero-Copy High-Frequency Trading Engine

## Objectives
- Implement an mmap ring buffer.
- Pack and unpack orders using struct.
- Generate mock orders using asyncio.
- Measure throughput and validate order transfer.

## Technologies
- Python
- mmap
- struct
- asyncio

## How to Run
python main.py

## Current Status
Week 1 prototype.

The producer and consumer currently run as
asynchronous tasks in the same Python process.
## Week 2: IPC Validation and Error Handling

- Validate order fields before writing them.
- Reject invalid orders.
- Detect when the ring buffer is full.
- Track generated, rejected, and failed orders.
- Test ring-buffer write and read operations.

## Run the Project

```bash
python main.py