# Videowall

A shell script to play random snippets from a collection of video files. 

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [ffmpeg](https://formulae.brew.sh/formula/ffmpeg)
- [VLC](https://www.videolan.org/vlc/)

## Setup

Drop `build_playlist.py` and `play_videowall.sh` into any folder that contains video files (`.mp4`, `.m4v`).

## Usage

Open `play_videowall.sh`.

### Options

These options determine the behavior of the videowall:

- `-c <HTML color hex>`  
  Tints all videos `<HTML color hex>`. (Defaults to `3b1e00`.)

  Example: `./play_videowall.sh -c 2e003b`

- `-f <string>`  
  Set the filename to `<string>`. Should be in format `filename.m3u`. (Defaults to name of current folder.)

  Example: `./play_videowall.sh -f party.m3u`

- `-t <integer>`  
  Set the duration of each video clip to `<integer>` seconds. (Defaults to 10 seconds.)

  Example: `./play_videowall.sh -t 30`
