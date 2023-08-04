import os
import re
from pydub import AudioSegment
from tinytag import TinyTag
from tqdm.auto import tqdm
from mutagen.flac import FLAC
from maroon.cue import parse_cue, Track


class Meta:
    def __init__(self, cue_path: str):
        self.cue_path = cue_path
        self.tracks = parse_cue(self.cue_path)
        self.wav_path = self.cue_path.replace(".cue", ".wav")
        self.original_metadata = TinyTag.get(self.wav_path)
        self.album_name, self.genre = self.get_album_name_and_genre()
        self.disc_number, self.total_discs = self.get_disc_info()

    def get_album_name_and_genre(self):
        default_album_name = self.get_default_album_name()
        album_name = input(f"Name of the album (default: {default_album_name}): ")
        album_name = album_name.strip() if album_name else default_album_name

        genre = input("Genre of the album (split by ; sign):")

        return album_name, genre

    def get_default_album_name(self):
        parent_folder = os.path.dirname(self.cue_path)
        match = re.search("DISC(\d+)", parent_folder)
        if match:
            # If the parent folder contains "DISC", use the grandparent folder name
            grandparent_folder = os.path.dirname(parent_folder)
            album_name = os.path.basename(grandparent_folder)
        else:
            # If the parent folder doesn't contain "DISC", use the parent folder name
            album_name = os.path.basename(parent_folder)

        # If the album name contains " - ", assume it follows the convention of "<artist> - <album>"
        if " - " in album_name:
            album_name = album_name.split(" - ")[-1]

        return album_name

    def get_disc_info(self):
        parent_folder = os.path.dirname(self.cue_path)
        disc_number = 1
        total_discs = 1
        match = re.search("DISC(\d+)", parent_folder)

        if match:
            disc_number = int(match.group(1))
            total_discs = 0
            for folder in os.listdir(os.path.dirname(parent_folder)):
                if "DISC" in folder:
                    total_discs += 1

        return disc_number, total_discs

    def get_metadata_dict(self, track: Track):
        return {
            "tracknumber": str(track.number),
            "tracktotal": str(len(self.tracks)),
            "discnumber": str(self.disc_number),
            "disctotal": str(self.total_discs),
            "album": self.album_name,
            "genre": self.genre,
        }


class Transform:
    def __init__(self, meta: Meta):
        self.meta = meta
        self.wav = AudioSegment.from_wav(self.meta.wav_path)
        self.split_tracks = self.split_wav()

    def get_end_time(self, index: int):
        if index == len(self.meta.tracks) - 1:
            return len(self.wav)
        else:
            return self.meta.tracks[index + 1].start_time

    def split_wav(self):
        split_tracks = []
        for i in range(len(self.meta.tracks)):
            track = self.meta.tracks[i]
            end_time = self.get_end_time(i)
            track_wav = self.wav[track.start_time: end_time]
            split_tracks.append((track, track_wav))
        return split_tracks

    def write_metadata_and_export(self, track: Track, track_wav: AudioSegment):
        output_filename = f"{str(track.number).zfill(2)}_{track.title}.flac"
        output_filepath = os.path.join(os.path.dirname(self.meta.cue_path), output_filename)
        track_wav.export(output_filepath, format="flac")

        flac = FLAC(output_filepath)
        flac["title"] = track.title if track.title else ""
        flac["artist"] = track.performer if track.performer else ""

        # Transfer original metadata to new FLAC file
        metadata_keys = []
        for attr in dir(self.meta.original_metadata):
            if not attr.startswith("__") and not callable(getattr(self.meta.original_metadata, attr)):
                metadata_keys.append(attr)

        for key in metadata_keys:
            value = getattr(self.meta.original_metadata, key)
            if value:
                flac[key] = str(value)

        # Add new metadata
        flac_metadata = self.meta.get_metadata_dict(track)

        for key, value in flac_metadata.items():
            flac[key] = value

        flac.save()

    def process(self):
        pbar = tqdm(self.split_tracks, desc=f"Splitting {os.path.basename(self.meta.cue_path).replace('.cue', '')}")
        for track, track_wav in pbar:
            self.write_metadata_and_export(track, track_wav)


class PostProcess:
    def __init__(self, meta: Meta, transform: Transform):
        self.meta = meta
        self.transform = transform

    def done(self):
        print(f"Split {len(self.meta.tracks)} tracks.")

def transform_folder(cue_path: str):
    meta = Meta(cue_path)
    transform = Transform(meta)
    transform.process()
    post_process = PostProcess(meta, transform)
    post_process.done()


if __name__ == "__main__":
    cue_path = r"X:\0音乐\Chinese\交工乐队 - 菊花夜行军\i\CDImage.cue"
    meta = Meta(cue_path)
    transform = Transform(meta)
    transform.process()
    post_process = PostProcess(meta, transform)
    post_process.done()
