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

- `-a`  
  Play video files alphabetically.

- `-c HTML_color`  
  Tint all videos `HTML_color`. (Default: `3b1e00`.)

  Example: `./videowall -c 2e003b`

- `-f format`  
  Set the playlist format. Options: `m3u`, `xspf`. (Default: `m3u`.)

  Example: `./videowall -f xspf`

- `-r`  
  Include video files in subfolders (recursively).

- `-t duration`  
  Set the duration of each video snippet. (Default: `10` seconds.)

  Example: `./videowall -t 30`
