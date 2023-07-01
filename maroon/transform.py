import os
import re
from pydub import AudioSegment
from tinytag import TinyTag
from tqdm.auto import tqdm
from mutagen.flac import FLAC
from maroon.cue import parse_cue, Track


class Meta:
    def __init__(self, cue_path):
        self.cue_path = cue_path
        self.tracks = parse_cue(self.cue_path)
        self.wav_path = self.cue_path.replace(".cue", ".wav")
        self.original_metadata = TinyTag.get(self.wav_path)
        self.album_name, self.genre = self.get_album_name_and_genre()
        self.disc_number, self.total_discs = self.get_disc_info()

    def get_album_name_and_genre(self):
        default_album_name = self.get_default_album_name()
        album_name = input(f"Enter the album name (default: {default_album_name}): ")
        album_name = album_name.strip() if album_name else default_album_name

        genre = input("Enter the genre of the album: ")

        return album_name, genre

    def get_default_album_name(self):
        parent_folder = os.path.dirname(self.cue_path)
        match = re.search("DISC(\d+)", parent_folder)
        if match:
            album_name = os.path.basename(os.path.dirname(parent_folder))
        else:
            album_name = os.path.basename(parent_folder)
        return album_name

    def get_disc_info(self):
        parent_folder = os.path.dirname(self.cue_path)
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


class Transform:
    def __init__(self, meta):
        self.meta = meta
        self.split_tracks = self.split_wav()

    def split_wav(self):
        wav = AudioSegment.from_wav(self.meta.wav_path)

        split_tracks = []
        for track in self.meta.tracks:
            end_time = (
                len(wav)
                if track == self.meta.tracks[-1]
                else self.meta.tracks[self.meta.tracks.index(track) + 1].start_time
            )
            track_wav = wav[track.start_time: end_time]
            split_tracks.append((track, track_wav))

        return split_tracks

    def write_metadata_and_export(self, track, track_wav):
        output_filename = f"{str(track.number).zfill(2)}_{track.title}.flac"
        output_filepath = os.path.join(os.path.dirname(self.meta.cue_path), output_filename)
        track_wav.export(output_filepath, format="flac")

        flac = FLAC(output_filepath)
        flac["title"] = track.title if track.title else ""
        flac["artist"] = track.performer if track.performer else ""

        # Transfer original metadata to new FLAC file
        metadata_keys = [
            attr
            for attr in dir(self.meta.original_metadata)
            if not attr.startswith("__") and not callable(getattr(self.meta.original_metadata, attr))
        ]
        for key in metadata_keys:
            value = getattr(self.meta.original_metadata, key)
            if value:
                flac[key] = str(value)

        # Add new metadata
        flac_metadata = {
            "tracknumber": str(track.number),
            "tracktotal": str(len(self.meta.tracks)),
            "discnumber": str(self.meta.disc_number),
            "disctotal": str(self.meta.total_discs),
            "album": self.meta.album_name,
            "genre": self.meta.genre,
        }

        for key, value in flac_metadata.items():
            flac[key] = value

        flac.save()

    def process(self):
        pbar = tqdm(self.split_tracks, desc=f"Splitting {os.path.basename(self.meta.cue_path).replace('.cue', '')}")
        for track, track_wav in pbar:
            self.write_metadata_and_export(track, track_wav)


class PostProcess:
    def __init__(self, meta, transform):
        self.meta = meta
        self.transform = transform

    def done(self):
        print(f"Split {len(self.meta.tracks)} tracks.")


if __name__ == "__main__":
    cue_path = r"D:\Andrew\Downloads\tmp\存流 - ARU\存流 - ARU.cue"
    meta = Meta(cue_path)
    transform = Transform(meta)
    transform.process()
    post_process = PostProcess(meta, transform)
    post_process.done()
