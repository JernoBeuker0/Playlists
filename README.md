# YouTube to Spotify Playlist Converter
I will make an actual README at some point, trust.

---

## To Use:
### Venv:
 - Make a venv using `requirements.txt`.

<br />

### Find the YouTube Playlist ID:
- Go to the playlist you want to copy.
- The URL should look something like: https://music.youtube.com/playlist?list=PL..
- Copy from and INCLUDING "PL" until the end of the line.

<br />

### Run the following command:
```bash
python -m app YT_PLAYLIST_ID NEW_PLAYLIST_NAME
```
Where NEW_PLAYLIST_NAME is (logically) the name of your new playlist. And YT_PLAYLIST_ID is the playlist ID you copied from before.

<br />

#### Optional arguments:
The run command can be extended with two optional arguments.
- The first is `-d`. This allows you to add your own description to the new Spotify Playlist.
- The second is `-p`. This prints all songs in the YouTube playlist to the terminal.

Find an example of a full command below:
```bash
python -m app YT_PLAYLIST_ID NEW_PLAYLIST_NAME -d "This is a description of this playlist" -p
```
