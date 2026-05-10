import asyncio
import keyboard
import yaml
import requests



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

# idk
async def timer(sleepTime, kt):
    print("timer function is now executing")
    await asyncio.sleep(sleepTime)
    kt.cancel()
    raise asyncio.TimeoutError


# updates the config.yml file
def updateConfigServerUrl():
    with open("forwarder.txt", "r") as f:
        newServerUrl = f.readline().strip()
        print(newServerUrl)
    
    # read config
    with open("config.yml", "r") as cfg:
        settings = yaml.safe_load(cfg)

    # change url
    settings["server-url"] = newServerUrl

    # write back to config
    with open("config.yml", "w") as cfg:
        yaml.dump(settings, cfg, default_flow_style=False)
    print("Successfully updated config to contain new server url.")


# sends a request to the backend
def sendRequest(count):
    serverUrl = getServerUrl()
    params = {
        "serverUrl":serverUrl,
        "device_id":getDeviceId(),
        "lon":"51.2376323",
        "lat":"1.2682091"
    }
    r = requests.post(url=serverUrl, params=params)
    if r.ok:
        print("request to server sent successfully")
    else:
        print(f"Error when transferring to server: {r.reason}")
    



# gets the server url from the config
def getServerUrl():
    with open("config.yml", "r") as cfg:
        return yaml.safe_load(cfg)["server-url"]
    

# gets the device id from the config
def getDeviceId():
    with open("config.yml", "r") as cfg:
        return yaml.safe_load(cfg)["device-id"]