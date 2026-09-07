import asyncio

# A coroutine with no `await` inside it never actually suspends -
# it runs start-to-finish in one go, just like a normal function call.
async def greet():
    return "Hello"

# asyncio.run() creates a new event loop on the current thread, runs the
# coroutine to completion on that loop, then closes the loop and returns
# the result. It blocks the caller until the coroutine is done.
message = asyncio.run(greet())

print(message)


async def greet1():
    print("Hello1")
    # await suspends this coroutine and hands control back to the event
    # loop. The loop has nothing else scheduled here, so it just waits
    # out the 5s timer before resuming greet1() at this exact point.
    await asyncio.sleep(5)
    print("World1")

asyncio.run(greet1())


async def worker(name, delay):
    print(f"{name} starting")
    # Each worker yields to the loop here. With multiple workers
    # in flight, the loop interleaves them instead of running one
    # fully before starting the next.
    await asyncio.sleep(delay)
    print(f"{name} finished after {delay}s")

async def main():
    # gather() schedules all three coroutines as concurrent tasks on the
    # same event loop (single thread). They all start immediately, then
    # each suspends at its `await asyncio.sleep`. The loop resumes
    # whichever task's timer fires first, so completion order follows
    # the delays (B, then C, then A), not the order they were started in.
    # Total wall-clock time is ~max(delays), not the sum of delays.
    await asyncio.gather(
        worker("A", 3),
        worker("B", 1),
        worker("C", 2),
    )

asyncio.run(main())
