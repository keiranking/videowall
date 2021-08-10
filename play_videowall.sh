#!/bin/sh

# Run relative to script location
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

help_prompt() {
  echo "Try '$(basename $0) -h' for more information."
}

help_text() {
  echo "  -a              Play videos alphabetically."
  echo "  -c HTML_color   Tint video files. (Default: '3b1e00')"
  echo "  -f format       Set playlist format {'m3u'|'xspf'}. (Default: 'm3u')"
  echo "  -h              Display this message."
  echo "  -r              Include files in subfolders."
  echo "  -t duration     Set duration of each video, in seconds. (Default: '10')"
}

usage_text() {
  echo "usage:"
  echo "  $(basename $0) [-ahr] [-c HTML_color] [-f format] [-t duration]"
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
        echo "error: Option '-${arg}' requires a valid 6-digit HTML color."
        help_prompt
        exit 1
      fi
      ;;
    f)
      playlist_format=${OPTARG}
      if [[ ! "$playlist_format" =~ ^(m3u|xspf)$ ]]
      then
        echo "error: Option '-${arg}' requires a valid playlist format {'m3u'|'xspf'}."
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
        echo "error: Option '-${arg}' requires a valid integer duration."
        help_prompt
        exit 1
      fi
      ;;
    \?)
      echo "error: Unknown option '-$OPTARG'." 1>&2
      usage_text
      exit 1
      ;;
    :)
      echo "error: Option '-$OPTARG' requires an argument."
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
