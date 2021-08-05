#!/bin/sh

# Run relative to script location
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Set defaults
playlist_name="$(basename "$PWD").m3u"
clip_duration_in_seconds=10
playlist_duration_in_hours=4
color_tint="3b1e00"
is_recursive=false

# Process flags and override defaults
optstring="c:f:rt:"
while getopts ${optstring} arg; do
  case "${arg}" in
    c) color_tint=${OPTARG};;
    f) playlist_name=${OPTARG};;
    r) is_recursive=true;;
    t) clip_duration_in_seconds=${OPTARG};;
  esac
done

echo "Generating playlist..."
python3 build_playlist.py $clip_duration_in_seconds $playlist_duration_in_hours "$playlist_name" $is_recursive
echo "Playing playlist..."
/Applications/VLC.app/Contents/MacOS/VLC --playlist-autostart --fullscreen --no-osd --loop --no-random --no-audio --video-filter "extract{component=0x$color_tint}" "$playlist_name"
