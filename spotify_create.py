import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

username =sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
client_id ='bb2e3fbb3d464ce2b843bf5f2bfeebf0'
client_secret='645eef3583144fb3ae92f3985ea1a94b'
redirect_uri ='http://google.com/'
# User ID: mms532?si=KP6bNPqvRvi0hprG-vsJ3g

#Erase cache and prompt for user persmission
try:
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

#Create spotifyObject
spotifyObject=spotipy.Spotify(auth=token)

# Get Current Device
devices = spotifyObject.devices()
track = spotifyObject.current_user_playing_track()
print()
if devices['devices'] ==[]:
    print("No Song is Currently Being Played")
else:
    deviceID = devices['devices'][0]['id']

    # Get currently playing Track and Artist 
    track = spotifyObject.current_user_playing_track()

    if track !=None:
        artist = track['item']['artists'][0]['name']
        name_track = track['item']['name']

        if artist != "":
            print("Currently Playing " + artist + " - " + name_track)
            webbrowser.open(track['item']['album']['images'][0]['url'])


user = spotifyObject.current_user()

displayName = user['display_name']
follower = user['followers']['total']

while True:
    print()
    print(">>>Welcome to Spotipy " + displayName + "!")
    print()
    print("0 - Search for an artist")
    print("1 - Exit")
    print()

    choice = input("Your choice: ")

    # Search for the artist
    if choice == "0": 
        print()
        searchQuery = input("What's the Artist Name?: ")
        print()

        # Get the search results
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")

        # Artist Details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0]) 
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # Album Details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract Album Data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM "+ item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract Track Data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()

        # See album art
        while True:
            songSelection = input("Enter a song number to see the album art and/or to change music if music is already playing (x to exit): ")
            if songSelection =="x":
                break
            devices_new = spotifyObject.devices()
            if devices_new['devices'] !=[]:
                deviceID_new = devices_new['devices'][0]['id']
                trackList = []
                trackList.append(trackURIs[int(songSelection)])
                spotifyObject.start_playback(deviceID_new, None, trackList)

            webbrowser.open(trackArt[int(songSelection)])

    # Ends the program
    if choice =="1":
        break

