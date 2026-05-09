def onMouseClick():
    print(f"Mouse button pressed")
    return True


class AsyncTimer:
    def __init__(self):
        self.currentTime = 0
        self.status = "none"

    def start(self, timems):
        pass

    def step(self, newTime):
        pass

