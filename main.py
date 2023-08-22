import pylast
import time
from colorama import Fore, Style
from os import system, name
import random 

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

API_KEY = "337f93cac1a69268c099201bbdebcdcc"
API_SECRET = "8e850397b6cfec36ef3374221a77cf07"

# Default Loop Delay
loop_delay = 0.2
count = 0;

clear()
system("title LastFM Scrobbler")
username = input(f"\n[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] User: ")
password = input(f"[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] Password: ")
password_hash = pylast.md5(password)
default_loop_delay = 3
artist = input(f"\n[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] Artist: ")
title = input(f"[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] Title: ")

try: 
    loop_delay = float(input(f"[{Fore.GREEN}>>{Fore.RESET}] Delay: "))
except ValueError:
    print(f"\n[{Fore.RED}XX{Fore.RESET}] Delay need to be an integer or decimal number.")
    print(f"[{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] Scrobbler will start scrobbling using the default delay ({Fore.GREEN}{Style.BRIGHT}{default_loop_delay}{Fore.RESET}).")
    loop_delay = default_loop_delay
print("")

lastfm = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)

while True:
    try:
        lastfm.scrobble(artist=artist, title=title, timestamp=int(time.time()))
        count +=1
        print(f"[{Fore.GREEN}{Style.BRIGHT}++{Fore.RESET}] Scrobbled [{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}] {artist} - {title} [{Fore.GREEN}{Style.BRIGHT}##{Fore.RESET}] ({count})")
    except pylast.WSError as e:
        print(f"[{Fore.RED}XX{Fore.RESET}] ERROR:", e)
    time.sleep(float(loop_delay))