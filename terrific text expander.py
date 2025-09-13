from pynput import keyboard
import pyautogui
import time

pressed_keys = set()

# Shortcut combos and their replacement texts
shortcuts = {
    frozenset(['b', 'r']): "be right back",
    frozenset(['t', 'y', 'l']): "talk to you later",
    frozenset(['a','f','k']): "away from keyboard"
}

# Flags to prevent retriggering
typed_flags = {combo: False for combo in shortcuts}

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            k = key.char.lower()
            pressed_keys.add(k)
        else:
            pressed_keys.add(key)

        # Check all defined shortcuts
        for combo, phrase in shortcuts.items():
            if combo.issubset(pressed_keys) and not typed_flags[combo]:
                print(f"Hotkey detected: typing '{phrase}'")
                pyautogui.press('backspace', presses=4)
                time.sleep(0.05)
                pyautogui.write(phrase)
                typed_flags[combo] = True

    except AttributeError:
        pass

def on_release(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            k = key.char.lower()
            pressed_keys.discard(k)
        else:
            pressed_keys.discard(key)
    except KeyError:
        pass

    # Reset typed flags when keys are released
    for combo in shortcuts:
        if not combo.issubset(pressed_keys):
            typed_flags[combo] = False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
