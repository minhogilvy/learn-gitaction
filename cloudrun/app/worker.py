import asyncio
from loguru import logger
from .modules.pubsub import create_and_run, config
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

async def initialize_app():
    logger.info("Application startup initiated")
    
    loop = asyncio.get_event_loop()

    # Initialize configuration in a non-blocking manner using run_in_executor
    configuration = await loop.run_in_executor(None, config.setup)

    subs = await loop.run_in_executor(
        None,
        config.load_subscriptions_from_paths,
        ['app.modules.pubsub.subs'],
        configuration.sub_prefix,
        configuration.filter_by
    )

    # Create and run subscriptions asynchronously
    await create_and_run(subs, configuration)
    
    logger.info("Application startup complete")

async def main():
    await initialize_app()

def serve():
    asyncio.run(main())

if __name__ == '__main__':
    num_processes = 1 # Number of CPU cores
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(serve) for _ in range(num_processes)]
        
        # Wait for all processes to complete
        for future in futures:
            future.result()