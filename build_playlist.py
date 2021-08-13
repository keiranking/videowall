import xml.etree.ElementTree as ET
import glob
import os
import random
import subprocess
import sys
import time
from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector

def find_closest_number(list, target, tolerance = 2):
    closest_value = min(list, key = lambda i: abs(i - target))
    if abs(closest_value - target) <= tolerance:
        return closest_value
    return target

def get_cuts(file, threshold = 12.0):
    video_manager = VideoManager([file])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold))
    video_manager.set_downscale_factor()

    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    return [round(scene.get_seconds(), 3) for scene in scene_manager.get_cut_list()]

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

def get_duration(file):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return int(float(result.stdout))

# Set defaults and override, if appropriate
intended_playlist_duration = 4*3600
# intended_playlist_duration = 60

clip_duration = 30
if len(sys.argv) >= 2:
    clip_duration = int(sys.argv[1])

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

is_optimized_for_cuts = True

# Get video files
files = []
for video_format in ["avi", "m4v", "mkv", "mov", "mp4", "mpeg", "mpg"]:
    files.extend(glob.glob(
        ("**/*." if is_recursive else "*.") + video_format,
        recursive = is_recursive))
file_durations = dict(zip(files,[get_duration(file) for file in files]))

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
            start_time = random.randint(0,file_durations[file] - clip_duration)
            if is_optimized_for_cuts:
                cuts = get_cuts(file)
                if cuts:
                    start_time = find_closest_number(cuts, start_time)
                    stop_time = start_time + clip_duration
                    stop_time = find_closest_number(cuts, stop_time)
            else:
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
