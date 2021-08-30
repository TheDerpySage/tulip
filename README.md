tulip
==============
Tulip is a bot made to listen in on MPD HTTP Streams. 

Currently, she's programmed to listen in on an MPD ogg stream hosted on the same host she's on, but this can theoretically work on other hosts. 

She's also programmed with some basic MPC commands, and the ability to inject youtube-dl streams into the playlist (This however has mixed results, youtube streams will randomly cut out).

DEPENDENCIES
=============
Python 3

pip install discord.py discord.py[voice]

youtube-dl and ffmpeg installed on the machine (in the same folder if on windows)

NOTE
=============
The "temp.py" files must be edited and the underscore temp removed from the
name before the application will run.
