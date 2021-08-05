import glob
import os
import random
import subprocess
import sys
import time 

def get_duration(file):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return int(float(result.stdout))

def playlist_item_text(file, file_duration, start_time, stop_time):
    return "#EXTINF:" + str(file_duration) + "," + file + "\n" \
        + "#EXTVLCOPT:start-time=" + str(start_time) + "\n" \
        + "#EXTVLCOPT:stop-time=" + str(stop_time) + "\n" \
        + file + "\n"

# Set defaults and override, if appropriate
clip_duration = 10
if len(sys.argv) >= 2:
    clip_duration = int(sys.argv[1])

intended_playlist_duration = 4*3600
if len(sys.argv) >= 3:
    intended_playlist_duration = int(sys.argv[2])*3600

playlist_name = os.path.split(os.getcwd())[1].lower() + ".m3u"
if len(sys.argv) >= 4:
    playlist_name = sys.argv[3]

is_recursive = False
if len(sys.argv) >= 5 and sys.argv[4] == 'true':
    is_recursive = True

# Create playlist
playlist = open(playlist_name, "w")
playlist.write("#EXTM3U" + "\n")

files = []
for extension in ["avi", "m4v", "mkv", "mp4", "mpeg"]:
    files.extend(glob.glob(
        ("**/*." if is_recursive else "*.") + extension,
        recursive = is_recursive))
file_durations = dict(zip(files,[get_duration(file) for file in files]))
current_playlist_duration = 0

while current_playlist_duration < intended_playlist_duration:
    random.shuffle(files)
    for file in files:
        start_time, stop_time = 0, file_durations[file]
        if file_durations[file] > clip_duration:
            start_time = random.randint(0,file_durations[file] - clip_duration)
            stop_time = start_time + clip_duration

        playlist.write(playlist_item_text(file, file_durations[file], start_time, stop_time))

        current_playlist_duration += clip_duration
        if current_playlist_duration >= intended_playlist_duration:
            break

playlist.close()

print(playlist_name + " created"
    " (" + time.strftime("%-Hhr %-Mmin", time.gmtime(current_playlist_duration)) +
    " from " + str(len(files)) + " files" + ")")
