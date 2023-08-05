from mutagen.flac import FLAC


class EditMeta:
    def __init__(self, audio_file_path: str):
        self.audio_file_path = audio_file_path
        self.flac = FLAC(self.audio_file_path)
        self.album_name, self.genre = self.get_album_name_and_genre()

    def get_album_name_and_genre(self):
        default_album_name = self.flac["album"][0] if "album" in self.flac else ""
        album_name = input(f"New name of the album (default: {default_album_name}): ")
        album_name = album_name.strip() if album_name else default_album_name

        default_genre = self.flac["genre"][0] if "genre" in self.flac else ""
        genre = input(f"New genre of the album (default: {default_genre}): ")
        genre = genre.strip() if genre else default_genre

        return album_name, genre

    def edit_metadata(self):
        self.flac["album"] = self.album_name
        self.flac["genre"] = self.genre
        self.flac.save()

    def process(self):
        self.edit_metadata()
        print(f"Edited metadata for {self.audio_file_path}.")


if __name__ == "__main__":
    audio_file_path = "/path/to/your/audio.flac"
    edit_meta = EditMeta(audio_file_path)
    edit_meta.process()
