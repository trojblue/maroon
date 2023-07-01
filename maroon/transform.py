import os
import re
import tinytag

from mutagen.flac import FLAC
from tqdm.auto import tqdm
from pydub import AudioSegment
from tinytag import TinyTag

from maroon.cue import parse_cue, Track


def get_original_metadata(wav_path: str):
    original_metadata = tinytag.TinyTag.get(wav_path)
    return original_metadata


def get_album_name(cue_path: str) -> str:
    """
    inputs a cue path and returns the default album name
    :param cue_path:  "something.cue"
    :return: album_name: str
    """
    parent_folder = os.path.dirname(cue_path)
    match = re.search("DISC(\d+)", parent_folder)
    if match:
        album_name = os.path.basename(os.path.dirname(parent_folder))
    else:
        album_name = os.path.basename(parent_folder)

    return album_name

def split_wav(wav_path: str, tracks: list[Track]) -> list[tuple[Track, AudioSegment]]:
    """
    Splits a WAV file into multiple tracks, according to <tracks> read from possibly a cue sheet.
    :param wav_path: something.wav
    :param tracks: cue sheet tracks (see maroon.cue.parse_cue)
    :return: pairs of (track_info, track_wav)
    """
    wav = AudioSegment.from_wav(wav_path)

    split_tracks = []
    for track in tracks:
        end_time = (
            len(wav)
            if track == tracks[-1]
            else tracks[tracks.index(track) + 1].start_time
        )
        track_wav = wav[track.start_time : end_time]
        split_tracks.append((track, track_wav))

    return split_tracks


def write_metadata_and_export(
    output_filepath: str,
    track: Track,
    track_wav: AudioSegment,
    original_metadata: TinyTag,
    total_tracks: int,
    disc_number: int,
    total_discs: int,
    album_name: str,
    genre: str,
) -> None:
    track_wav.export(output_filepath, format="flac")

    flac = FLAC(output_filepath)
    flac["title"] = track.title if track.title else ""
    flac["artist"] = track.performer if track.performer else ""

    metadata_keys = [
        attr
        for attr in dir(original_metadata)
        if not attr.startswith("__") and not callable(getattr(original_metadata, attr))
    ]

    for key in metadata_keys:
        value = getattr(original_metadata, key)
        if value:
            flac[key] = str(value)

    flac["tracknumber"] = str(track.number)
    flac["tracktotal"] = str(total_tracks)

    flac["discnumber"] = str(disc_number)
    flac["disctotal"] = str(total_discs)

    flac["album"] = album_name
    flac["genre"] = genre

    flac.save()


def get_disc_info(cue_path: str) -> tuple[int, int]:
    """
    inputs a cue path and returns the disc number and total discs
    :param cue_path:  "something.cue"
    :return: (disc_number, total_discs): int, int
    """
    parent_folder = os.path.dirname(cue_path)
    disc_number = 1
    total_discs = 1
    match = re.search("DISC(\d+)", parent_folder)
    if match:
        disc_number = int(match.group(1))
        total_discs = len(
            [
                folder
                for folder in os.listdir(os.path.dirname(parent_folder))
                if "DISC" in folder
            ]
        )
    return disc_number, total_discs

def split_wav_from_cue(cue_path: str) -> None:
    """
    :param cue_path: "something.cue"
    :return:
    """
    tracks = parse_cue(cue_path)
    original_metadata = get_original_metadata(cue_path.replace(".cue", ".wav"))
    split_tracks = split_wav(cue_path.replace(".cue", ".wav"), tracks)

    disc_number, total_discs = get_disc_info(cue_path)

    if not original_metadata.album:
        default_album_name = get_album_name(cue_path)
        album_name = input(f"Enter the album name (default: {default_album_name}): ")
        album_name = album_name.strip() if album_name else default_album_name
    else:
        album_name = original_metadata.album

    genre = input("Enter the genre of the album: ")

    pbar = tqdm(
        split_tracks, desc=f"Splitting {os.path.basename(cue_path).replace('.cue', '')}"
    )

    for track, track_wav in pbar:
        output_filename = f"{str(track.number).zfill(2)}_{track.title}.flac"
        output_filepath = os.path.join(os.path.dirname(cue_path), output_filename)

        write_metadata_and_export(
            output_filepath,
            track,
            track_wav,
            original_metadata,
            len(tracks),
            disc_number,
            total_discs,
            album_name,
            genre,
        )

    # print(f'Split {len(tracks)} tracks.')


if __name__ == "__main__":
    split_wav_from_cue(
        # r"X:\0音乐\VSinger\音楽的同位体 星界 1st COMPILATION ALBUM メタファー\DISC1\星界 - 詩想のメタファー.cue"
        r"D:\Andrew\Downloads\tmp\存流 - ARU\存流 - ARU.cue"
    )
