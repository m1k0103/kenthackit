import requests
from func import AsyncTimer
import asyncio



async def main():
    print("started")

    # create AsyncTimer object
    timer = AsyncTimer(2000)
    
    async with asyncio.TaskGroup() as tg:
        task = tg.create_task(timer.start())
    print(f"Task execution complete. Result: {task.result}")

    
    #await timer.start()
    #await timer.click()
    #await timer.click()

    quit()

    # wait for an input (mouse click in the future)
    #while True:
    #    input("waiting")
    #    timer.start()
    #    timer.click()
    #    print("clicked")
        
     
        



if __name__ == "__main__":
    #main()
    asyncio.run(main())
