#!/bin/sh

# Run relative to script location
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

function help_text {
  echo "Options and arguments:"
  echo "-c <color>    tint video files; <color> must be 6-digit hexadecimal"
  echo "-f <format>   set playlist format ['m3u', 'xspf']"
  echo "-h            print this help message and exit"
  echo "-r            include video files in subfolders (recursively)"
  echo "-t <integer>  set duration of each video to <integer> seconds"
}

function usage_text {
  echo "Usage: ./play_videowall.sh [-c <color>] [-f <format>]"
  echo "    [-h] [-r] [-t <integer>]"
}

# Set defaults
playlist_format="m3u"
playlist_name="$(basename "$PWD")"
clip_duration_in_seconds=10
playlist_duration_in_hours=4
color_tint="3b1e00"
is_recursive=false

# Process flags and override defaults
optstring=":c:f:hrt:"
while getopts ${optstring} arg; do
  case "${arg}" in
    c) color_tint=${OPTARG};;
    f) playlist_format=${OPTARG};;
    h)
      usage_text
      echo
      help_text
      exit 0
      ;;
    r) is_recursive=true;;
    t) clip_duration_in_seconds=${OPTARG};;
    ?)
      echo "Unknown option: -$OPTARG" 1>&2
      usage_text
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

echo "Generating playlist..."
python3 build_playlist.py $clip_duration_in_seconds $playlist_duration_in_hours "$playlist_name" $playlist_format $is_recursive
echo "Playing playlist..."
/Applications/VLC.app/Contents/MacOS/VLC --playlist-autostart --fullscreen --no-osd --loop --no-random --no-audio --video-filter "extract{component=0x$color_tint}" "$playlist_name.$playlist_format"
