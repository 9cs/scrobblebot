import pylast
import time
from colorama import Fore, Style, init
from os import system, name
import random 

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def get_valid_float_input(prompt, default_value):
    try:
        value = float(input(prompt))
        return value
    except ValueError:
        print(f"\n[{Fore.RED}XX{Fore.RESET}] Invalid input. Using the default value: {default_value}")
        return default_value
    
init(autoreset=True)

API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

# Default Loop Delay
loop_delay = 0.3
count = 0
default_loop_delay = loop_delay

clear()
system("title LastFM Scrobbler")
username = input(f"\n[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] User: ")
password = input(f"[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] Password: ")
password_hash = pylast.md5(password)

artist = input(f"\n[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] Artist: ")
title = input(f"[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] Title: ")

try: 
    loop_delay = get_valid_float_input(f"[{Fore.GREEN}>>{Fore.RESET}] Delay: ", default_loop_delay)
except ValueError:
    print(f"\n[{Fore.RED}XX{Fore.RESET}] Delay need to be an integer or decimal number.")
    print(f"[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] Scrobbler will start scrobbling using the default delay ({Fore.GREEN}{Style.BRIGHT}{default_loop_delay}{Fore.RESET}).")
    loop_delay = default_loop_delay
    
print(f"\n[{Fore.YELLOW}!!{Fore.RESET}] Press Ctrl+C to stop the scrobbler.")
print("")

lastfm = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)

try:
    while True:
        try:
            lastfm.scrobble(artist=artist, title=title, timestamp=int(time.time()))
            count += 1
            print(f"[{Fore.GREEN}{Style.BRIGHT}++{Fore.RESET}] Scrobbled [{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] {artist} - {title} [{Fore.GREEN}{Style.BRIGHT}##{Fore.RESET}] ({count})")
        except pylast.WSError as e:
            print(f"[{Fore.RED}XX{Fore.RESET}] ERROR:", e)
        time.sleep(float(loop_delay))
except KeyboardInterrupt:
    print(f"\n[{Fore.YELLOW}!!{Fore.RESET}] Scrobbler stopped.")