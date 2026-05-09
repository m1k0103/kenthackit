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
            #keyboard.add_hotkey('enter', lambda: timer.click())

            # listen for input
            print("listening for input")
            keyboard.wait('enter')
            if keyboard.is_pressed("enter"):
                
                deadline = asyncio.get_running_loop().time() + 5000 # change to 0.5 later
                timeout.reschedule(deadline)

                print("rescheduling deadline")
                await asyncio.create_task(timer.readKeyboardInput())

                #await timer.readKeyboardInput()
                print(timeout.expired())

            #print("deadline expired")
            #r = await timer.result()
            #print(r)

    # if time runs out, 
    except asyncio.TimeoutError:
        pass
    
    r = await timer.result()
    print(r)


if __name__ == "__main__":
    asyncio.run(main())
