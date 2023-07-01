import os
from collections import namedtuple
from pydub import AudioSegment

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


def split_wav_from_cue(cue_path):
    tracks = parse_cue(cue_path)
    wav_path = cue_path.replace('.cue', '.wav')
    wav = AudioSegment.from_wav(wav_path)

    for track in tracks:
        end_time = len(wav) if track == tracks[-1] else tracks[tracks.index(track) + 1].start_time
        track_wav = wav[track.start_time:end_time]

        output_filename = f'{str(track.number).zfill(2)}_{track.title}.wav'
        track_wav.export(output_filename, format='wav')

    print(f'Split {len(tracks)} tracks.')


if __name__ == '__main__':
    # Example usage:
    split_wav_from_cue(r'X:\0音乐\VSinger\音楽的同位体 星界 1st COMPILATION ALBUM メタファー\DISC1\星界 - 詩想のメタファー.cue')
