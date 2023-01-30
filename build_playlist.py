from moviepy.editor import *
import csv
import glob
import os
import random
import sys
import time
import xml.etree.ElementTree as ET

def get_duration(file):
    sys.stdout.write("\033[K" + "Processing " + file + "\r")
    return VideoFileClip(file).duration

def generate_playlist_item_text(file, duration, start_time, stop_time, format = "m3u"):
    if format == "m3u":
        return "#EXTINF:" + str(duration) + "," + file + "\n" \
            + "#EXTVLCOPT:start-time=" + str(start_time) + "\n" \
            + "#EXTVLCOPT:stop-time=" + str(stop_time) + "\n" \
            + file + "\n"
    elif format == "xspf":
        track_tag = ET.Element("track")

        location_tag = ET.SubElement(track_tag, "location")
        location_tag.text = file

        duration_tag = ET.SubElement(track_tag, "duration")
        duration_tag.text = str(duration)

        extension_tag = ET.SubElement(track_tag, "extension")
        extension_tag.set("application", "http://www.videolan.org/vlc/playlist/0")

        start_time_tag = ET.SubElement(extension_tag, "vlc:option")
        start_time_tag.text = f"start-time={start_time}"
        stop_time_tag = ET.SubElement(extension_tag, "vlc:option")
        stop_time_tag.text = f"stop-time={stop_time}"

        return track_tag

def generate_playlist_text(items, format = "m3u"):
    if format == "m3u":
        return "#EXTM3U" + "\n" + "".join(items)
    elif format == "xspf":
        playlist_tag = ET.Element("playlist")
        playlist_tag.set("version", "1")
        playlist_tag.set("xmlns", "http://xspf.org/ns/0/")
        playlist_tag.set("xmlns:vlc", "http://www.videolan.org/vlc/playlist/ns/0/")

        trackList_tag = ET.SubElement(playlist_tag, "trackList")
        for item in items:
            trackList_tag.append(item)

        ET.indent(ET.ElementTree(playlist_tag))
        return ET.tostring(playlist_tag, encoding = "unicode", xml_declaration = True)

# Set defaults and override, if appropriate
clip_duration = 30
if len(sys.argv) >= 2:
    clip_duration = int(sys.argv[1])

intended_playlist_duration = 4*3600
if len(sys.argv) >= 3:
    intended_playlist_duration = int(sys.argv[2])*3600

playlist_name = os.path.split(os.getcwd())[1]
if len(sys.argv) >= 4:
    playlist_name = sys.argv[3]

playlist_format = "m3u"
if len(sys.argv) >= 5:
    playlist_format = sys.argv[4]
playlist_name += f".{playlist_format}"

is_recursive = False
if len(sys.argv) >= 6 and sys.argv[5] == 'true':
    is_recursive = True

is_alphabetical = False
if len(sys.argv) >= 7 and sys.argv[6] == 'true':
    is_alphabetical = True

# Get video files
files = []
for video_format in ["avi", "m4v", "mkv", "mov", "mp4", "mpeg", "mpg"]:
    files.extend(glob.glob(
        ("**/*." if is_recursive else "*.") + video_format,
        recursive = is_recursive))

# Retrieve video durations from durations file
file_durations = {}
if os.path.exists("durations.txt"):
    with open("durations.txt", newline = "") as durations_list:
        reader = csv.reader(durations_list, delimiter="\t")
        for video in reader:
            file_durations[video[0]] = float(video[1])

# Cull durations of deleted videos
for file in list(file_durations.keys()):
    if file not in files:
        file_durations.pop(file, None)

# Add new video durations
for file in files:
    if file not in file_durations:
        file_durations[file] = get_duration(file)

# Update durations file
with open("durations.txt", "w+") as durations_list:
    writer = csv.writer(durations_list, delimiter="\t")
    for key, value in file_durations.items():
        writer.writerow([key, value])

if is_alphabetical:
    files.sort()
    intended_playlist_duration = len(files) * clip_duration

# Assemble playlist items
playlist_items = []
current_playlist_duration = 0
while current_playlist_duration < intended_playlist_duration:
    if not is_alphabetical:
        random.shuffle(files)

    for file in files:
        start_time, stop_time = 0, file_durations[file]
        if file_durations[file] > clip_duration:
            start_time = random.randint(0,int(file_durations[file]) - clip_duration)
            stop_time = start_time + clip_duration

        playlist_items.append(generate_playlist_item_text(file, file_durations[file], start_time, stop_time, playlist_format))

        current_playlist_duration += clip_duration
        if current_playlist_duration >= intended_playlist_duration:
            break

# Create playlist file
playlist = open(playlist_name, "w")
playlist.write(generate_playlist_text(playlist_items, playlist_format))
playlist.close()

print(playlist_name + " created"
    " (" + time.strftime("%-Hhr %-Mmin", time.gmtime(current_playlist_duration)) +
    " from " + str(len(files)) + " files" + ")")
