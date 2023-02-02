# Videowall

A shell script to play random snippets from a collection of video files.

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [ffmpeg](https://formulae.brew.sh/formula/ffmpeg)
- [VLC](https://www.videolan.org/vlc/)

## Setup

Copy `build_playlist.py` and `videowall` into any folder that contains video files.

## Usage

1. In your terminal, navigate to the folder with your video files.

1. Run `./videowall`.

### Options

These options determine the behavior of the videowall:

- `-a, --sort`  
  Play video files alphabetically by filename.

- `-c, --color HTML_color`  
  Tint all videos `HTML_color`. (Default: `3b1e00`.)

  Example: `./videowall -c 2e003b`

- `-f, --format format`  
  Set the playlist format. Options: `m3u`, `xspf`. (Default: `m3u`.)

  Example: `./videowall -f xspf`

- `-r, --recursive`  
  Include video files in subfolders (recursively).

- `-s, --speed speed`  
  Set playback speed. Normal speed is 1.0. (Default: `0.618`.)

  Example: `./videowall -s 2.0`

- `-t, --time duration`  
  Set the duration of each video snippet. (Default: `30` seconds.)

  Example: `./videowall -t 10`

- `-x, --no-effects`  
  Remove all audio and video effects.
