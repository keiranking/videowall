# Videowall

A shell script to play random snippets from a collection of video files. 

## Requirements

- Python 3
- ffmpeg
- VLC, a video player app

## Setup

Drop `build_playlist.py` and `play_videowall.sh` into any folder that contains video files (`.mp4`, `.m4v`).

## Usage

Open `play_videowall.sh`.

### Options

These options determine the behavior of the videowall:

- `-t <integer>`  
  Set the duration of each video clip to `<integer>` seconds. (If not supplied, defaults to 10 seconds.)

- `-f <string>`  
  Set the filename to `<string>`. Should be in format `filename.m3u`. (If not supplied, defaults to name of current folder.)

### Example

- `./play_videowall.sh -t 15 -f party.m3u`  
  Builds and plays playlist `party.m3u` with random 15-sec video clips.
