# Videowall

A shell script to play random snippets from a collection of video files. 

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [ffmpeg](https://formulae.brew.sh/formula/ffmpeg)
- [VLC](https://www.videolan.org/vlc/)

## Setup

Drop `build_playlist.py` and `play_videowall.sh` into any folder that contains video files.

## Usage

Open `play_videowall.sh`.

### Options

These options determine the behavior of the videowall:

- `-c <HTML color hex>`  
  Tint all videos `<HTML color hex>`. (Defaults to `3b1e00`.)

  Example: `./play_videowall.sh -c 2e003b`

- `-f <format>`  
  Set the playlist format to `<format>`. Options: `m3u`, `xspf`. (Defaults to `m3u`.)

  Example: `./play_videowall.sh -f xspf`

- `-r`  
  Include video files in subfolders (recursively).

  Example: `./play_videowall.sh -r`

- `-t <integer>`  
  Set the duration of each video clip to `<integer>` seconds. (Defaults to 10 seconds.)

  Example: `./play_videowall.sh -t 30`
