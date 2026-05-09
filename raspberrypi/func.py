import asyncio
import keyboard

class Counter:
    def __init__(self):

        self.clicks = 0
        #self.loop = asyncio.new_event_loop()
        #self.task = None


    ## Start the timer
    #async def start(self):
    #    # if the timer is not running and still hasnt 
    #    if (self.status == "done") & (self.ms != 0):
    #        self.status == "running"
#
    #        self.task = self.loop.create_task(self.step())
    #        self.loop.run_forever()
    #        
    #    if self.status == "running":
    #        print("is already running. do nothing")
    #    
    #    try:
    #        self.loop.run_until_complete(self.task)
    #        print("started loop")
    #    finally:
    #        return self.clicks



    # Step. Decrease the amount of milliseconds remaining.
    #async def step(self):
    #    #if self.ms > 0:
    #    #    self.ms -= 1
    #    #    return self.ms
    #    #else:
    #    #    return False
    #    while status == "running":
    #        if self.ms > 0:
    #            self.ms -= 1
    #            print(self.ms)
    #            await asyncio.sleep(0.001) # Wait 1 ms. Check again if time has ran out.
    #        else:
    #            print("Timer has finished")
    #            self.status = "done"
    #            self.loop.stop()
    #            done()
    #    

        # No more steps to do. No more time



    # Increment click count 
    def click(self):
        self.clicks += 1
        print(f"clicks: {self.clicks}")


    async def result(self):
        print(f"No more time left. Clicks detected: {self.clicks}")
        return self.clicks


    async def readKeyboardInput(self):
        x = 1 # starts at 1 press because of the initial press to activate the program
        keyboard.add_hotkey('enter', lambda: self.click())
        keyboard.wait()
        print("function readKeyboardInput finished executing")




