def parse_cue(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    tracks = []
    track_data = {}

    for line in lines:
        if "TRACK" in line:
            if track_data:
                # Append previous track data
                tracks.append(track_data)
                track_data = {}
        elif "INDEX 01" in line:
            # Extract minutes, seconds and frames
            time_parts = line.split('INDEX 01 ')[-1].split(':')
            track_data['minutes'] = int(time_parts[0])
            track_data['seconds'] = int(time_parts[1])
            track_data['frames'] = int(time_parts[2])

    if track_data:
        # Append last track data
        tracks.append(track_data)

    return tracks


import os
from pydub import AudioSegment
from pydsmid.cuesheet import Cuesheet


def split_wav_from_cue(directory, cue_filename):
    cue_path = os.path.join(directory, cue_filename)

    # Load cue sheet
    cue = Cuesheet(cue_path)
    cue.parse()

    # Load wav file
    wav_filename = cue_filename.replace('.cue', '.wav')
    wav_path = os.path.join(directory, wav_filename)
    wav = AudioSegment.from_wav(wav_path)

    # Create output directory if it doesn't exist
    output_dir = os.path.join(directory, "split_files")
    os.makedirs(output_dir, exist_ok=True)

    for i, track in enumerate(cue.tracks, start=1):
        # Calculate start and end times in milliseconds
        start_time = int(track.index[1].time.min * 60 * 1000
                         + track.index[1].time.sec * 1000
                         + track.index[1].time.frame * 1000 / 75)
        end_time = len(wav) if i == len(cue.tracks) else int(cue.tracks[i].index[1].time.min * 60 * 1000
                                                             + cue.tracks[i].index[1].time.sec * 1000
                                                             + cue.tracks[i].index[1].time.frame * 1000 / 75)

        # Extract part of wav file
        track_wav = wav[start_time:end_time]

        # Save track wav file
        output_filename = f'{track.performer} - {track.title}.wav'
        output_path = os.path.join(output_dir, output_filename)
        track_wav.export(output_path, format="wav")

    print(f'Split {len(cue.tracks)} tracks.')
