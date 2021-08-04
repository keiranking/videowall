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

path = os.getcwd()
clip_duration = int(sys.argv[1]) if len(sys.argv) >= 2 else 10
intended_playlist_duration = int(sys.argv[2])*3600 if len(sys.argv) >= 3 else 4*3600
print(clip_duration, intended_playlist_duration)
playlist_name = (sys.argv[3] if len(sys.argv) >= 4 
    else os.path.split(path)[1].lower() + ".m3u")

current_playlist_duration = 0

_m3u = open(playlist_name, "w")
_m3u.write("#EXTM3U" + "\n")
files = glob.glob("*.m*4*")
while current_playlist_duration < intended_playlist_duration:
    random.shuffle(files)
    for file in files:
        file_duration = get_duration(file)
        start_time = random.randint(0,file_duration - clip_duration) if file_duration > clip_duration else 0
        stop_time = start_time + clip_duration if file_duration > clip_duration else file_duration

        _m3u.write(playlist_item_text(file, file_duration, start_time, stop_time))
        current_playlist_duration += file_duration
_m3u.close()

print(playlist_name + " created"
    " (" + str(len(glob.glob("*.m*4*"))) + " files" +
    ", " + time.strftime("about %-Hhr %-Mmin", time.gmtime(current_playlist_duration)) + ")")
