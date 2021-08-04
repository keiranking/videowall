#!/bin/sh

# Run relative to script location
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$PARENT_PATH"

# Set defaults
PLAYLIST_NAME="$(basename "$PWD").m3u"
CLIP_DURATION_IN_SECONDS=10
PLAYLIST_DURATION_IN_HOURS=4

# Process flags and override defaults
optstring="f:t:"
while getopts ${optstring} arg; do
  case "${arg}" in
    f) PLAYLIST_NAME=${OPTARG};;
    t) CLIP_DURATION_IN_SECONDS=${OPTARG};;
  esac
done

echo "Creating playlist..."
python3 build_playlist.py $CLIP_DURATION_IN_SECONDS $PLAYLIST_DURATION_IN_HOURS $PLAYLIST_NAME
echo "Playing playlist..."
/Applications/VLC.app/Contents/MacOS/VLC --playlist-autostart --fullscreen --no-osd --loop --no-random --no-audio --video-filter "extract{component=0x3b1e00}" $PLAYLIST_NAME
