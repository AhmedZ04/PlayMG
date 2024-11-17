import ctypes
from ctypes import wintypes
import time


user32 = ctypes.WinDLL('user32', use_last_error=True)
wintypes.ULONG_PTR = ctypes.POINTER(ctypes.c_ulong)


INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12
VK_H = 0x48
VK_A = 0x41
VK_W = 0x57
VK_K = 0x4B
VK_SPACE = 0x20
VK_T = 0x54
VK_U = 0x55
VK_ENTER = 0x0D
VK_S = 0x53
VK_D = 0x44
VK_LEFT = 0x25
VK_RIGHT = 0x27

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)
            
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def TypeKey(hexKeyCode):
    PressKey(hexKeyCode)
    ReleaseKey(hexKeyCode)


def HawkTuah():
    # Spit On That Thang 😂😂😂
    TypeKey(VK_H)
    TypeKey(VK_A)
    TypeKey(VK_W)
    TypeKey(VK_K)
    TypeKey(VK_SPACE)
    TypeKey(VK_T)
    TypeKey(VK_U)
    TypeKey(VK_A)
    TypeKey(VK_H)
    TypeKey(VK_ENTER)

def PressW():
    PressKey(VK_W)
    time.sleep(0.3)
    ReleaseKey(VK_W)

def PressA():
    PressKey(VK_A)
    time.sleep(0.3)
    ReleaseKey(VK_A)

def PressS():
    PressKey(VK_S)
    time.sleep(0.3)
    ReleaseKey(VK_S)

def PressD():
    PressKey(VK_D)
    time.sleep(0.3)
    ReleaseKey(VK_D)

def PressSpace():
    PressKey(VK_SPACE)
    time.sleep(0.3)
    ReleaseKey(VK_SPACE)


def PressRightArrow():
    PressKey(VK_RIGHT)
    time.sleep(0.3)
    ReleaseKey(VK_RIGHT)


def PressLeftArrow():
    PressKey(VK_LEFT)
    time.sleep(0.3)
    ReleaseKey(VK_LEFT)




if __name__ == '__main__':
    time.sleep(3)
    HawkTuah()
    

