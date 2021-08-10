#!/bin/sh

# Run relative to script location
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

function help_prompt {
  echo "Try '$(basename $0) -h' for more information"
}

function help_text {
  echo "Options and arguments:"
  echo "-c <color>    tint video files; <color> must be 6-digit hexadecimal"
  echo "-f <format>   set playlist format ['m3u', 'xspf']"
  echo "-h            print this help message and exit"
  echo "-r            include video files in subfolders (recursively)"
  echo "-t <integer>  set duration of each video to <integer> seconds"
}

function usage_text {
  echo "Usage: $(basename $0) [-hr] [-c <color>] [-f <format>] [-t <integer>]"
}

# Set defaults
playlist_format="m3u"
playlist_name="$(basename "$PWD")"
clip_duration_in_seconds=10
playlist_duration_in_hours=4
color_tint="3b1e00"
is_alphabetical=false
is_recursive=false

# Process flags and override defaults
optstring=":ac:f:hrt:"
while getopts ${optstring} arg; do
  case "${arg}" in
    a) is_alphabetical=true;;
    c)
      color_tint=${OPTARG}
      if [[ ! "$color_tint" =~ ^([[:xdigit:]]{6})$ ]]
      then
        echo "error: '$color_tint' is not a valid color"
        help_prompt
        exit 1
      fi
      ;;
    f)
      playlist_format=${OPTARG}
      if [[ ! "$playlist_format" =~ ^(m3u|xspf)$ ]]
      then
        echo "error: '$playlist_format' is not a valid playlist format"
        help_prompt
        exit 1
      fi
      ;;
    h)
      usage_text
      echo
      help_text
      exit 0
      ;;
    r) is_recursive=true;;
    t)
      clip_duration_in_seconds=${OPTARG}
      if [[ ! "$clip_duration_in_seconds" =~ ^([0-9]+)$ ]]
      then
        echo "error: '$clip_duration_in_seconds' is not a valid integer"
        help_prompt
        exit 1
      fi
      ;;
    \?)
      echo "Unknown option: -$OPTARG" 1>&2
      usage_text
      exit 1
      ;;
    :)
      echo "Option '-$OPTARG' requires an argument"
      usage_text
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

echo "Generating playlist..."
python3 build_playlist.py $clip_duration_in_seconds $playlist_duration_in_hours "$playlist_name" $playlist_format $is_recursive $is_alphabetical
echo "Playing playlist..."
/Applications/VLC.app/Contents/MacOS/VLC --playlist-autostart --fullscreen --no-osd --loop --no-random --no-audio --video-filter "extract{component=0x$color_tint}" "$playlist_name.$playlist_format"
