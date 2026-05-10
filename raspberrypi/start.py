import requests
import asyncio
import keyboard
from func import Counter, timer, sendRequest, updateConfigServerUrl, getServerUrl, getDeviceId
import yaml



# https://superfastpython.com/asyncio-timeout/
async def loop():
    print("loop started")

    SLEEPTIME = 1

    # create AsyncTimer object
    counter = Counter()

    kt = asyncio.create_task(counter.readKeyboardInput())
    t = asyncio.create_task(timer(SLEEPTIME,kt))

    try:
        # Wait for initial key press
        keyboard.wait('enter')
        print("initial enter key has been pressed")

        await t
        await kt
    except asyncio.TimeoutError:
        print("Time has ran out.")

    result = counter.result()
    print(result)
    sendRequest(result) #should work??


# main function to run all the other code
async def main():
    updateConfigServerUrl()

    while True:
        await loop()
    


if __name__ == "__main__":
    asyncio.run(main())
