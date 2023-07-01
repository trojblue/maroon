import os
import click
from .rename import rename_music_folder
from .transform import transform_folder


@click.group()
def cli():
    pass


def process_directory(directory: str) -> None:
    """Process a directory recursively, formatting music folders and splitting .wav files from .cue sheets"""
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if "DISC" in dir:
                rename_music_folder(os.path.join(root, dir))

        for file in files:
            if file.endswith(".cue"):
                cue_path = os.path.join(root, file)
                transform_folder(cue_path)


@cli.command()
@click.argument("dir_name")
def format(dir_name: str):
    # Tidy implementation
    print(f"Tidying directory: {dir_name}")
    process_directory(dir_name)


@cli.command()
@click.argument("dir_name")
def edit(dir_name):
    # Placeholder for your new function
    print(f"Editing directory: {dir_name}")
    # Call your new function here


if __name__ == "__main__":
    cli()
