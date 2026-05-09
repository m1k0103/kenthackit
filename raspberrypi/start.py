import requests
import asyncio
import keyboard
from func import AsyncTimer




# https://superfastpython.com/asyncio-timeout/
async def main():
    print("started")

    # create AsyncTimer object
    timer = AsyncTimer()
    
    
    try:
        async with asyncio.timeout(None) as timeout:
            keyboard.add_hotkey('enter', lambda: timer.click())

            # listen for input
            print("listening for input")
            keyboard.wait()
            if keyboard.is_pressed("enter"):
                
                deadline = asyncio.get_running_loop().time() + 2 # change to 0.5 later
                timeout.reschedule(deadline)
                print("enter pressed. rescheduling deadline")


    except asyncio.TimeoutError:
        r = timer.result()
        print(r)
        

if __name__ == "__main__":
    asyncio.run(main())
