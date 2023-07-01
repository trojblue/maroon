import os
import re
import tinytag
from collections import namedtuple
from pydub import AudioSegment
from mutagen.flac import FLAC
from tqdm.auto import tqdm

Track = namedtuple('Track', ['number', 'title', 'performer', 'start_time'])


def parse_cue(cue_path):
    with open(cue_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tracks = []
    current_track = None

    for line in lines:
        if line.startswith('  TRACK'):
            if current_track:
                tracks.append(current_track)
            track_number = int(line.split()[1])
            current_track = Track(number=track_number, title=None, performer=None, start_time=None)

        elif line.startswith('    TITLE'):
            current_track = current_track._replace(title=line.split('"')[1])

        elif line.startswith('    PERFORMER'):
            current_track = current_track._replace(performer=line.split('"')[1])

        elif line.startswith('    INDEX'):
            time_str = line.split()[2]
            mins, secs, frames = map(int, time_str.split(':'))
            start_time = (mins * 60 + secs + frames / 75) * 1000  # Convert to milliseconds
            current_track = current_track._replace(start_time=int(start_time))

    if current_track:
        tracks.append(current_track)

    return tracks


def get_disc_info(cue_path):
    parent_folder = os.path.dirname(cue_path)
    disc_number = 1
    total_discs = 1
    match = re.search('DISC(\d+)', parent_folder)
    if match:
        disc_number = int(match.group(1))
        total_discs = len([folder for folder in os.listdir(os.path.dirname(parent_folder)) if 'DISC' in folder])
    return disc_number, total_discs


def split_wav_from_cue(cue_path):
    tracks = parse_cue(cue_path)
    wav_path = cue_path.replace('.cue', '.wav')
    wav = AudioSegment.from_wav(wav_path)

    # Getting metadata from original file
    original_metadata = tinytag.TinyTag.get(wav_path)

    # Getting disc info
    disc_number, total_discs = get_disc_info(cue_path)

    for track in tqdm(tracks):
        end_time = len(wav) if track == tracks[-1] else tracks[tracks.index(track) + 1].start_time
        track_wav = wav[track.start_time:end_time]

        output_filename = f'{str(track.number).zfill(2)}_{track.title}.flac'
        output_filepath = os.path.join(os.path.dirname(cue_path), output_filename)
        track_wav.export(output_filepath, format='flac')

        # Writing metadata to the new file
        flac = FLAC(output_filepath)

        # Assigning title and artist from cue
        if track.title:
            flac["title"] = track.title
        if track.performer:
            flac["artist"] = track.performer

        # Assigning other metadata from original file
        metadata_keys = [attr for attr in dir(original_metadata) if
                         not attr.startswith('__') and not callable(getattr(original_metadata, attr))]
        for key in metadata_keys:
            value = getattr(original_metadata, key)
            if value:
                flac[key] = str(value)

        # Assigning track number and total track number
        flac['tracknumber'] = str(track.number)
        flac['tracktotal'] = str(len(tracks))

        # Assigning disc number and total disc number
        flac['discnumber'] = str(disc_number)
        flac['disctotal'] = str(total_discs)

        flac.save()

    print(f'Split {len(tracks)} tracks.')


if __name__ == '__main__':
    split_wav_from_cue(r'X:\0音乐\VSinger\音楽的同位体 星界 1st COMPILATION ALBUM メタファー\DISC1\星界 - 詩想のメタファー.cue')
