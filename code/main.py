from utility.runtime import simulated_runtime, yield_task, sleep


async def main():
    print(f'Time: {simulated_runtime.timestamp}')
    await yield_task()
    print(f'Time: {simulated_runtime.timestamp}')
    await sleep(1)
    print(f'Time: {simulated_runtime.timestamp}')
    await sleep(10)
    print(f'Time: {simulated_runtime.timestamp}')
    await sleep(int(1e9))
    print(f'Time: {simulated_runtime.timestamp}')

if __name__ == "__main__":
    simulated_runtime.create_task(main())
    simulated_runtime.run()
