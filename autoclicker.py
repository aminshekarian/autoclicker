import time
from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def query_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y

# کشیدن توابع مورد نیاز بیرون حلقه
SetCursorPos = windll.user32.SetCursorPos
mouse_event = windll.user32.mouse_event
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

print("Please position your mouse where you want to click and wait.")
time.sleep(5)
mouse_pos = query_mouse_position()

start_time = time.time()
duration = 30  # 30 seconds
interval = 0.15001  # 210 milliseconds

print("Autoclicker started.")

while (time.time() - start_time) < duration:
    SetCursorPos(mouse_pos[0], mouse_pos[1])
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(interval)

print("Autoclicker finished.")
