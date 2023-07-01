import os
import click
from .format import format_music_folder
from .transform import split_wav_from_cue


@click.command()
@click.argument("dir_name")
def cli(dir_name):
    # Tidy implementation
    print(f"Tidying directory: {dir_name}")
    format_music_folder(dir_name)

    # for each subdir with name DISCx: run split_wav_from_cue
    for subdir in os.listdir(dir_name):
        if "DISC" in subdir:
            # find cue file(s) in subdir
            for file in os.listdir(os.path.join(dir_name, subdir)):
                if file.endswith(".cue"):
                    cue_path = os.path.join(dir_name, subdir, file)
                    split_wav_from_cue(cue_path)
                    break


if __name__ == "__main__":
    cli()
