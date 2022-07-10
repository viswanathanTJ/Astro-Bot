from user import User
import os
from time import sleep
import pyautogui as p
import psutil
import win32print
from geopy.geocoders import Nominatim
import subprocess
import pyperclip
from AstroBot import logger

location = None

def open_astro():
    if "KKcAstro.exe" in (p.name() for p in psutil.process_iter()):
        os.system("TASKKILL /F /IM KKcAstro.exe")
    p.hotkey('win', 'down')
    os.startfile("C:\KkcAstro\KkcAstro.exe")
    sleep(3)
    p.click(53,38)
    p.click(61,81)
    p.click(172,86)


def horoscope(user):
    open_astro()

    if user.gender[0] == 'f' or user.gender[0] == 'F' or user.gender[0] == 'P' or user.gender == 'p':
        p.click(1056,416)
        p.click(841,419)

    print(user)
    p.click(752, 493)
    sleep(1)
    p.typewrite(user.date)
    p.press('right')
    p.typewrite(user.month)
    p.press('right')
    p.typewrite(user.year)
    p.press('tab')
    p.typewrite(user.hours)
    p.press('right')
    p.typewrite(user.minutes)
    p.press('right')
    p.press('right')
    p.typewrite(user.ampm[0])
    p.press('tab')
    p.press('tab')
    if location is None:
        p.typewrite(user.place)
        p.press('down')
        if 'salem' in user.place or 'Salem' in user.place:
            p.press('down')
    else:
        fill_location(user.place)

    p.hotkey('alt', 'g')

def dd2dms(latitude, longitude):
    dd = abs(latitude)
    minutes, seconds = divmod(dd*3600, 60)
    degrees, minutes = map(int, divmod(minutes, 60))
    side = 'N' if latitude >= 0 else 'S'
    lat =  [str(degrees).zfill(2), str(minutes).zfill(3), side]
    dd = abs(longitude)
    minutes, seconds = divmod(dd*3600, 60)
    degrees, minutes = map(int, divmod(minutes, 60))
    side = 'E' if longitude >= 0 else 'W'
    lon = [str(degrees).zfill(3), str(minutes).zfill(3), side]
    return lat, lon

def load_foreign():
    from PIL import ImageGrab
    import pytesseract as pt

    pt.pytesseract.tesseract_cmd = r'C:\Users\HARI\AppData\Local\Tesseract-OCR\tesseract.exe'
    x, y = 865, 536
    box = (x, y, x+38, y+17)
    im = ImageGrab.grab(box).resize((500, 300))
    crct_text = pt.image_to_string(im, lang='eng')
    print(crct_text)
    chh, cmm = map(int, crct_text.strip().split('-'))
    p.hotkey('alt', 'c')
    x, y = 745, 580
    box = (x, y, x+29, y+14)
    im = ImageGrab.grab(box).resize((500, 300))
    text = pt.image_to_string(im)
    hh, mm = map(int, text.strip().split('.'))
    p.click(884, 587) # time
    crct_whole = chh*100 + (50 if cmm else 0)
    wrong = hh*100 + (50 if mm else 0)
    times = crct_whole - wrong
    if times < 0: dir = 'up'
    else: dir = 'down'
    for _ in range(abs(times//50)):
        p.press(dir)

def fill_location(place):
    print(location.address)
    loc = location.raw['address']
    code = loc['country_code']
    country = loc['country']
    p.typewrite(place.capitalize()+' '+loc['state']+' '+code.upper())
    p.press('tab')
    lat, long = dd2dms(location.latitude, location.longitude)
    p.typewrite(lat[0]+lat[1])
    p.press('tab')
    p.typewrite(lat[2])
    p.press('tab')
    p.typewrite(long[0]+long[1])
    p.press('tab')
    p.typewrite(long[2])
    if country != 'India':
        p.click(1236, 633)
        if code.lower() == 'lk':
            p.typewrite('Sri Lanka')
        else:
            p.typewrite(country)
        p.hotkey('alt', 'e')
        load_foreign()

def is_printer_off():
    phandle = win32print.OpenPrinter('HP LaserJet M1005')
    attributes = win32print.GetPrinter(phandle)[13]
    is_offline = (attributes & 0x00000400) >> 10
    if is_offline:
        return True
    return False

def confirm_print():
    if "KKcAstro.exe" in (p.name() for p in psutil.process_iter()):
        if not is_printer_off():
            return False, 'பிரின்டர் ஆன் பண்ணவும்'
        p.click(218, 33)
        p.click(360, 413)
        return True
    return False, 'ஜாதகம் இல்லை. டீடைல் அனுப்பவும்'

def send():
    plist = (p.name() for p in psutil.process_iter())
    if "KKcAstro.exe" in plist:
        file_name = "horoscope"
        file_path = "C:\KkcAstro\horoscope.pdf"
        if os.path.exists(file_path):
            logger.info("Removed %s", file_path)
            os.remove(file_path)
        if os.path.exists("C:\KkcAstro\horoscope.jpg"):
            logger.info("Removed %s", file_path)
            os.remove("C:\KkcAstro\horoscope copy.jpg")
        # if "Photoshop.exe" in plist:
        #     os.system("TASKKILL /F /IM Photoshop.exe")
        p.press('esc')
        p.click(325, 35)
        sleep(.2)
        p.typewrite(file_name)
        sleep(.2)
        p.press('enter')
        sleep(.1)
        p.press('enter')
        os.startfile("C:\Program Files\Adobe\Adobe Photoshop CS4 (64 Bit)\Photoshop.exe")
        sleep(2)
        p.hotkey('ctrl', 'o')
        sleep(.5)
        p.typewrite(file_path)
        sleep(.2)
        p.press('enter')
        p.press('enter')
        p.press('f3')
        sleep(3.5)
        os.system("TASKKILL /F /IM Photoshop.exe")
        return True
    return False

def cancel():
    if "KKcAstro.exe" in (p.name() for p in psutil.process_iter()):
        os.system("TASKKILL /F /IM KKcAstro.exe")

def check_city(name):
    global location
    location = None
    with open('india.txt', 'r') as f:
        if name in f.read():
            logger.info('Found city in india.txt')
            return True
    geolocator = Nominatim(user_agent="viswa_2k")
    location = geolocator.geocode(name, exactly_one=True, addressdetails=True)
    if location is None:
        return None
    logger.info('Found city by API', location.raw['address'])
    return True

def delete_print_queue():
    phandle = win32print.OpenPrinter('HP LaserJet M1005')
    print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
    for job in print_jobs:
        win32print.SetJob(phandle, job['JobId'], 0, None, win32print.JOB_CONTROL_DELETE)
    logger.info("Deleted %s jobs", len(print_jobs))
    win32print.ClosePrinter(phandle)
    

def scan(fpath):
    if is_printer_off():
        print('Printer is offline')
        return False
    p.hotkey('win', 'down')
    os.startfile(
        "C:\Program Files\Adobe\Adobe Photoshop CS4 (64 Bit)\Photoshop.exe")
    sleep(4)
    p.click(1137, 423)
    p.press('f2')
    sleep(1)
    p.press('enter')
    p.hotkey('alt', 'c')
    p.hotkey('alt', 's')
    sleep(20)
    p.hotkey('alt', 'f4')
    os.rename('I:\\Customers\\Horoscope\\IMG.jpg', fpath)
    logger.info('Scanned successfully')
    return True

def send_whatsapp(fpath):
    subprocess.run([r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe', 'web.whatsapp.com'])
    pyperclip.copy(fpath)
    sleep(5)
    p.click(431, 262)
    # p.hotkey('ctrl', 'b') # camera icon
    p.click(725, 995) # pin icon
    p.click(724, 928) # camera icon
    sleep(.2)
    # p.typewrite(fpath)
    p.hotkey('ctrl', 'v')
    p.press('enter')
    sleep(1)
    p.click(1710, 972) # send icon
    # p.hotkey('ctrl', 'x') # send icon
    sleep(1)
    # p.hotkey('ctrl', 'q') # doc icon
    p.click(725, 995) # pin icon
    p.click(708, 725) # doc icon
    sleep(.3)
    # p.typewrite(fpath)
    p.hotkey('ctrl', 'v')
    p.press('enter')
    sleep(1)
    # p.hotkey('ctrl', 'x') # send icon
    p.click(1710, 972) # send icon
    logger.info('Sent successfully')
