import asyncio
import keyboard

class Counter:
    def __init__(self):
        self.clicks = 1


    # Increment click count 
    def click(self):
        self.clicks += 1
        print(f"clicks: {self.clicks}")


    async def readKeyboardInput(self):
        x = 1 # starts at 1 press because of the initial press to activate the program
        keyboard.add_hotkey('enter', lambda: self.click())
        print("function readKeyboardInput finished executing")


    # Get final results after being terminated
    def result(self):
        print(f"No more time left. Clicks detected: {self.clicks}")
        return self.clicks


async def timer(sleepTime, kt):
    print("timer function is now executing")
    await asyncio.sleep(sleepTime)
    kt.cancel()
    raise asyncio.TimeoutError



def sendRequest(count):
    
    pass