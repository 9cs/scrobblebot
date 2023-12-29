import pylast, time, requests, pwinput
from colorama import Fore, Style, init
from os import system, name

init(autoreset=True)
API_KEY = """5ebce83b48c27d7ab97c03719a8c2372"""
API_SECRET = "b6f703957fc8f46bb9f81e270bc2d0f1"
GET_INFOS = "http://ws.audioscrobbler.com/2.0/"

def debugFunc():
    params = {
    'method': 'user.getInfo',
    'user': 'stream',
    'api_key': API_KEY,
    'format': 'json'
    }
    response = requests.get(GET_INFOS, params=params)
    data = response.json()
    print(data)

default_loop_delay = 0.3
count = 0
exc = f"""{Fore.YELLOW}{Style.BRIGHT}!!{Fore.RESET}"""
pas = f"""{Fore.GREEN}{Style.BRIGHT}>>{Fore.RESET}"""
err = f"""{Fore.RED}{Style.BRIGHT}XX{Fore.RESET}"""
pos = f"""{Fore.GREEN}{Style.BRIGHT}++{Fore.RESET}"""
pys = f"""{Fore.YELLOW}{Style.BRIGHT}>>{Fore.RESET}"""

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
        print(f"\n[{err}] Invalid input. Using the default value: {default_value}")
        return default_value

clear()

def getUser():
    global user
    params = {
    'method': 'user.getInfo',
    'user': {username},
    'api_key': API_KEY,
    'format': 'json'}
    response = requests.get(GET_INFOS, params=params)
    data = response.json()
    user = data['user']['realname']
    if user == "":
        user = data['user']['name']

def getCreds():
    global username
    global password
    global password_hash
    username = input(f"\n[{pas}] User: ")
    password = pwinput.pwinput(prompt=f'[{pas}] Password: ', mask='*')
    password_hash = pylast.md5(password)

def getDelay():
    global loop_delay
    try: 
            loop_delay = get_valid_float_input(f"[{pas}] Delay: ", default_loop_delay)
            print('')
    except ValueError:
        print(f"\n[{err}] Delay need to be an integer or decimal number.")
        print(f"[{pas}] Application will start working using the default delay ({Fore.GREEN}{Style.BRIGHT}{default_loop_delay}{Fore.RESET}).")
        loop_delay = default_loop_delay

def getArtist():
    global artistName
    ArtistUrl = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={API_KEY}&format=json"
    response = requests.get(ArtistUrl)
    data = response.json()
    artistName = data['artist']['name']

def getAlbumByName():
    global album
    global albumName
    global albumSongs
    params = {
    'method': 'album.getInfo',
    'artist': {artistName},
    'album': {albumTitle},
    'api_key': API_KEY,
    'format': 'json'
    }
    try:
        response = requests.get(GET_INFOS, params=params)
        data = response.json()
        albumName = data['album']['name']
        albumSongs = [track["name"] for track in data["album"]["tracks"]["track"]]
    except KeyError:
        albumName = data['track']['name']

def getAlbumBySong():
    global albumName
    global songName
    params = {
    'method': 'track.getInfo',
    'artist': {artist},
    'track': {title},
    'api_key': API_KEY,
    'format': 'json'
    }
    try:
        response = requests.get(GET_INFOS, params=params)
        data = response.json()
        albumName = data['track']['album']['title']
        songName = data['track']['name']
    except KeyError:
        songName = data['track']['name']
        albumName = songName

def unique():
    try:
        count = 0
        while True:
            try:
                lastfm.update_now_playing(artist=artistName, title=title, album=albumName, duration=30)
                lastfm.scrobble(artist=artistName, title=title, album=albumName, timestamp=int(time.time()))
                count += 1
                print(f"[{pos}] Scrobbled [{pas}] {artistName} - {songName} [{Fore.GREEN}{Style.BRIGHT}##{Fore.RESET}] ({count})")
            except pylast.WSError as e:
                print(e)
    except KeyboardInterrupt:
        print(f"\n[{exc}] Scrobbler stopped.")
        time.sleep(5)
        clear()
        menu()
    except pylast.WSError:
        status = pylast.WSError.details()
        if status == 29:
            print("rate limited troxa")

def multiple():
    try:
        count = 0
        while True:
            for i in albumSongs:
                try:
                    lastfm.scrobble(artist=artistName, title=i, album=albumName, timestamp=int(time.time()))
                    count += 1
                    print(f"[{pos}] Scrobbled [{pas}] {artistName} - {i} [{Fore.GREEN}{Style.BRIGHT}##{Fore.RESET}] ({count})")
                except pylast.WSError as e:
                    print(f"[{err}] ERROR:", e)
                time.sleep(float(loop_delay))
    except KeyboardInterrupt:
        print(f"\n[{exc}] Scrobbler stopped.")
        time.sleep(5)
        clear()
        menu()

def menu():
    global lastfm
    lastfm = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)
    while True:
        global artist
        print(f"\n[{exc}] Select a scrobbling mode:")
        print(f"[{exc}] 1: {Fore.YELLOW}{Style.BRIGHT}SINGLE{Fore.RESET} song scrobbling")
        print(f"[{exc}] 2: {Fore.YELLOW}{Style.BRIGHT}FULL{Fore.RESET} album scrobbling")
        choice = input(f"[{pys}] Mode: ")
        artist = input(f"\n[{pas}] Artist: ")
        if choice == '1':
            global title
            title = input(f"[{pas}] Title: ") 
            getArtist()
            getAlbumBySong()
            getDelay()   
            print(f"[{exc}] Press Ctrl+C to stop the scrobbler.")
            print("")
            unique()
        elif choice == '2':
            global albumTitle
            albumTitle = input(f"[{pas}] Album title: ")
            getArtist()
            getAlbumByName()
            getDelay()
            print(f"[{exc}] Press Ctrl+C to stop the scrobbler.")
            print("")
            multiple()
        else:
            print(f"\n[{err}] Invalid input. Try again.")
            time.sleep(3)
            clear()
            menu()

def Start():
    try:
        clear()
        getCreds()
        getUser()
        system(f"title LastFM Scrobbler - User: {user}")
        menu()
    except pylast.WSError:
        print(f"\n[{err}] Invalid credentials. Try again.")
        time.sleep(3)
        Start()

Start()
