import click
from .format import format_music_folder

@click.command()
@click.argument('dir_name')
def cli(dir_name):
    # Tidy implementation
    print(f'Tidying directory: {dir_name}')
    format_music_folder(dir_name)

if __name__ == '__main__':
    cli()
