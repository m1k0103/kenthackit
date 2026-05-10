import keyboard

def on_key_press():
    print("You pressed enter")

keyboard.add_hotkey('enter', on_key_press)
keyboard.wait()
