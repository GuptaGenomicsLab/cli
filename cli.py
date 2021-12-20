import click

from scripts.fetch_prots.command import fetch_prots


@click.group()
def gtools():
    pass


gtools.add_command(fetch_prots)

if __name__ == '__main__':
    gtools()
