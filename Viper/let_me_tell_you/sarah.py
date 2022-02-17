import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\m.bischof\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
img = cv2.imread(r'C:\Users\m.bischof\Pictures\canyoureadthis.PNG')
# img = cv2.resize(img, (720,480))
# cv2.imshow('Result',img)
# cv2.waitKey(0)
# hImg, wImg, _ = img.shape
# boxes = pytesseract.pytesseract.image_to_boxes(img)
# for b in boxes.splitlines():
#     b = b.split(' ')
#     print(b)
#     x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
#     cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 1)
#     cv2.putText(img, b[0], (x, hImg - y + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 205, 50), 1)

# cv2.imshow('Detected text', img)
# cv2.waitKey(0)
from PIL import ImageGrab
import string
import win32gui
import time
import enchant
from pynput.keyboard import Key, Controller
keyboard = Controller()
d_spell = enchant.Dict("en_US")
toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

firefox = [(hwnd, title) for hwnd, title in winlist if 'windows powershell' in title.lower()]
# just grab the hwnd for first window matching firefox
firefox = firefox[0]
hwnd = firefox[0]
print(hwnd,type(hwnd))

win32gui.SetForegroundWindow(hwnd)
bbox = win32gui.GetWindowRect(hwnd)
while 1:
    all_s = []
    start = time.perf_counter()
    while time.perf_counter() - start < 1:
        img = ImageGrab.grab(bbox)
        # img.show()
        s = pytesseract.image_to_string(img)
        if "quit?" in s:
            keyboard.type('\n')
            time.sleep(0.1)
            continue

    
            s = ''.join([x for x in s if x in string.printable])
        all_s.append(s)
    dick = {}
    for s in all_s:
        if s == "": continue
        if s in dick.keys():
            dick[s] += 1
        else:
            dick[s] = 1
    if len(dick) == 0: continue
    true_dick = {x:0 for x in dick.keys()}
    for i in true_dick.keys():
        words = i.split(' ')
        for word in words:
            true_dick[i] += int(d_spell.check(word))
    best_i = -1
    best_sum = -1
    for i,value in true_dick.items():
        if value > best_sum:
            best_sum = value
            best_i = i
        if value == best_sum:
            if dick[i] > dick[best_i]:
                best_i = i
    print(best_i)

    # keyboard.type(best_i)

    for c in best_i:
        keyboard.press(c)
        time.sleep(0.001)
        keyboard.release(c)
