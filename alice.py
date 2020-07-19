import datetime
import os
import subprocess
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from ctypes import *
import geocoder
import pyaudio
import pyttsx3
import speech_recognition as sr
import json
import ssl
import webbrowser

#CERTIFICATE HANDLING
ctx = ssl.create_default_context()
ctx.check_hostname = None
ctx.verify_mode = ssl.CERT_NONE


#ERROR HANDLING FOR ALSA
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


#FUNCTION DEFINITIONS
def internetConnectivity():
    try:
        urllib.request.urlopen('https://www.duckduckgo.com')
        return True
    except:
        return False

def activeWallpaper():
    subprocess.call("feh --bg-fill /home/wolfian/Pictures/mega_charizard_x.jpg", shell=True)

def inactiveWallpaper():
    subprocess.call("feh --bg-fill /home/wolfian/Pictures/mega_charizard_x2.jpg", shell=True)

def weather():
    loc = geocoder.ip('me') #fetching current location based on ipaddress
    url = "https://fcc-weather-api.glitch.me/api/current?lat=" + str(loc.latlng[0])+"&lon=" + str(loc.latlng[1])
    data = urllib.request.urlopen(url, context=ctx).read().decode()
    report = json.loads(data)
    if report['cod'] == 200:
        # str(report['coord']['lat']) + ' latitude. ' +str(report['coord']['lon']) + ' longitute.'
        fianl_report = 'Current location: ' + str(report['name']) + '. Weather type: ' + str(report['weather'][0]['main']) + '. Wind speed: ' + str(report['wind']['speed']) + ' metre per second. Temperature: ' + str(report['main']['temp']) + ' degree celcius. Humidity: ' + str(report['main']['humidity'])
    else:
         fianl_report = 'Unable to fetch weather report!'
    # print(fianl_report)
    return fianl_report

def speak(rule, keyword = ''):
    os.system('clear')
    activeWallpaper()
    print("Archangel speaking ...")

    #-1 = ready to listen
    if rule == -1:
        engine.say("order me SENPAI!")

    #0 = startup wish
    if rule == 0:
        hour = int(datetime.datetime.now().hour)
        if hour >=0 and hour < 12:
            engine.say('Good morning SENPAI!')
        elif hour >=12 and hour < 18:
            engine.say('Good afternoon SENPAI!')
        else:
            engine.say('Good evening SENPAI!')

    #1 = check for internet connection
    if rule == 1: 
        checker = internetConnectivity()
        if checker == False:
            engine.say('System offline')
            engine.runAndWait()
            os.system('clear')
            inactiveWallpaper()
            return False
        elif checker == True:
            engine.say('System online')
            engine.runAndWait()
            os.system('clear')
            inactiveWallpaper()
            return True

    #2 = weather report of my location
    if rule == 2:
        engine.say(weather())

    #3 = opening
    if rule == 3:
        engine.say('opening '+keyword)

    #4 = closing
    if rule == 4:
        engine.say('closing')

    #5 = what to search on duckduckgo?
    if rule == 5:
        engine.say('What do you want me to search on Duck Duck Go?')

    #6 = what to search on youtube?
    if rule == 6:
        engine.say('What do you want me to search on youtube?')
    
    #7 = searching
    if rule == 7:
        engine.say('searching!')

    #10 = goodbye
    if rule == 10:
        # print('Archangel closing ...')
        engine.say('Bye-bye SENPAI!')
        engine.runAndWait()
        inactiveWallpaper()
        time.sleep(1)
        subprocess.call("/home/wolfian/Scripts/discharge.sh &>/dev/null & disown", shell=True)
        os.system('clear')
        quit()

    #11 = did not understand
    if rule == 11:
        engine.say("Sorry, I didn't understand that! I'm such a dumb bot!")
    
    #12 = when ignored
    if rule == 12:
        engine.say("Notice me,SENPAI!")

    #13 = weather report?
    if rule == 13:
        engine.say("Shall I proceed with the weather report?")

    #14 = never mind
    if rule == 14:
        engine.say("Never mind!")

    engine.runAndWait()
    inactiveWallpaper()
    os.system('clear')


def command(call):
    r = sr.Recognizer()
    with noalsaerr(), sr.Microphone() as source:
        os.system('clear')
        print(networkStatus)

        if call == 1:
            print('Idle ...')
        if call == 2:
            print('Listening ...')
        
        r.pause_threshold = 1
        r.energy_threshold = 494
        r.adjust_for_ambient_noise(source) #, duration=0.5)
        try:
            # print('listen start')
            audio = r.listen(source, timeout=5)
            # print('listen stop')
            query = r.recognize_google(audio, language='eng-in').lower()
            print('Response captured: ',query)
            time.sleep(1)
            if 'system' in query or 'call' in query:
                return 'Enhance Armament'
        except:
            return 'f'
        if len(query)>1:
            return query.lower()
        else:
            return 'f'


# PROGRAM STARTS HERE
engine = pyttsx3.init('espeak')
engine.setProperty('voice', 'en+f2')
engine.setProperty('rate',140)

subprocess.call("killall discharge.sh", shell=True)
inactiveWallpaper()
time.sleep(1)
speak(0)
time.sleep(1)

networkStatus = ''
status = speak(1)
time.sleep(1)
flag1 = internetConnectivity() # to notify only when internet conectivity status is altered

#weather report
speak(13)
answer = command(2)
if 'yes' in answer:
    speak(2)
elif 'no' in answer:
    pass
else:
    speak(14)


# main loop
while True:    
    #getting initiation command 
    while True:
        # checking internet connectivity before each iteration
        status = internetConnectivity()
        if status == True:
            networkStatus = '- Archaengel online -'
        else:
            networkStatus = '- Archangel offline -'
        if flag1 != status: # checking change in internet connectivity
            flag1 = speak(1)
        # print('status: ', status)
        # print('flag1: ', flag1)
        # time.sleep(1)
        call1 = command(1)
        if call1 == 'Enhance Armament':
            speak(-1)
            break
    timeout = time.time() + 10
    
    # getting actual command
    while True:
        if time.time() > timeout:
            break
        call2 = command(2)
        if call2 != 'f':
            break
        
    # openening certain application
    if 'open' in call2:
        if 'firefox' in call2:
            subprocess.call("firefox &", shell=True)
            speak(3, 'Firefox')
        elif 'chrome' in call2 or 'google' in call2:
            subprocess.call("google-chrome &", shell=True)
            subprocess.call("google-chrome-stable &", shell=True)
            speak(3, 'Google chrome')
        elif 'code' in call2 or 'visual studio' in call2:
            subprocess.call("code &", shell=True)
            speak(3, 'Visual Studio Code')
        elif 'team' in call2 or 'teams' in  call2 or 'microsoft' in call2:
            subprocess.call("teams", shell=True)
            speak(3, 'Microsoft Teams')
        elif 'spotify' in call2:
            subprocess.call("spotify &", shell=True)
            speak(3, 'Spotify')
        else:
            speak(11)

    # closing certain application
    elif 'close' in call2:
        if 'firefox' in call2:
            speak(4, 'Firefox')
            subprocess.call("killall firefox &", shell=True)
        elif 'chrome' in call2 or 'google' in call2:
            speak(4, 'Google chrome')
            subprocess.call("killall google-chrome &", shell=True)
            subprocess.call("killall google-chrome-stable &", shell=True)
            subprocess.call("killall chrome &", shell=True)
        elif 'code' in call2 or 'visual studio' in call2:
            speak(4, 'Visual Studio Code')
            subprocess.call("killall code &", shell=True)
        elif 'team' in call2 or 'teams' in  call2 or 'microsoft' in call2:
            speak(4, 'Microsoft Teams')
            subprocess.call("killall teams &", shell=True)
        elif 'spotify' in call2:
            subprocess.call("killall spotify &", shell=True)
            speak(4, 'Spotify')
        else:
            speak(11)

    # searching on duckduckgo
    elif 'search' in call2:
        speak(5)
        search = command(2)
        url = 'https://duckduckgo.com/?q=' + search
        webbrowser.get('firefox').open_new_tab(url)
        speak(7)

    # searching on youtube
    elif 'youtube' in call2:
        speak(6)
        search = command(2)
        url = 'https://youtube.com/results?search_query=' + search
        webbrowser.get('firefox').open_new_tab(url)
        speak(7)

    # controlling spotify
    elif 'music' in call2:
        #play/pause
        subprocess.call("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause &", shell=True)
        os.system('clear')

    # cancel, exit, unable to understand, shutdown, suspend, reboot
    elif 'shutdown' in call2:
        subprocess.call("shutdown -r now", shell=True)

    elif 'reboot' in call2:
        subprocess.call("reboot", shell=True)

    elif 'sleep' in call2:
        subprocess.call("systemctl suspend", shell=True)

    elif 'cancel' in call2:
        continue
    
    elif 'exit' in call2:
        os.system('clear')
        speak(10)
    
    elif 'f' in call2:
        speak(12)
    
    else:
        speak(11)