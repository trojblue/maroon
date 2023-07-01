"""
This module contains functions for parsing CUE files.
"""

from collections import namedtuple

Track = namedtuple("Track", ["number", "title", "performer", "start_time"])


def parse_cue(cue_path) -> list[Track]:
    with open(cue_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    tracks = []
    current_track = None

    for line in lines:
        if line.startswith("  TRACK"):
            if current_track:
                tracks.append(current_track)
            track_number = int(line.split()[1])
            current_track = Track(
                number=track_number, title=None, performer=None, start_time=None
            )

        elif line.startswith("    TITLE"):
            current_track = current_track._replace(title=line.split('"')[1])

        elif line.startswith("    PERFORMER"):
            current_track = current_track._replace(performer=line.split('"')[1])

        elif line.startswith("    INDEX"):
            time_str = line.split()[2]
            mins, secs, frames = map(int, time_str.split(":"))
            start_time = (
                mins * 60 + secs + frames / 75
            ) * 1000  # Convert to milliseconds
            current_track = current_track._replace(start_time=int(start_time))

    if current_track:
        tracks.append(current_track)

    return tracks
