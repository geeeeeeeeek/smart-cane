import asyncio

async def looper():
    for i in range(1_000_000_000):
        print(f'Printing {i}')
        await asyncio.sleep(0.5)

async def main():
    print('Starting')
    future = asyncio.ensure_future(looper())

    print('Waiting for a few seconds')
    await asyncio.sleep(4)

    print('Cancelling')
    future.cancel()

    print('Waiting again for a few seconds')
    await asyncio.sleep(2)

    print('Done')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())