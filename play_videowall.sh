#!/bin/sh

# Run relative to script location
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$PARENT_PATH"

PLAYLIST_NAME="$(basename "$PWD").m3u"

# echo "Creating playlist..."
# python3 create_playlist.py $PLAYLIST_NAME
# echo "Playing playlist..."
# /Applications/VLC.app/Contents/MacOS/VLC --playlist-autostart --fullscreen --no-osd --random --no-audio --video-filter "extract{component=0x3b1e00}" $PLAYLIST_NAME

CLIP_DURATION_IN_SECONDS=10
PLAYLIST_DURATION_IN_HOURS=4

echo "Creating playlist..."
python3 build_playlist.py $CLIP_DURATION_IN_SECONDS $PLAYLIST_DURATION_IN_HOURS $PLAYLIST_NAME
echo "Playing playlist..."
/Applications/VLC.app/Contents/MacOS/VLC --playlist-autostart --fullscreen --no-osd --loop --no-audio --video-filter "extract{component=0x3b1e00}" $PLAYLIST_NAME
