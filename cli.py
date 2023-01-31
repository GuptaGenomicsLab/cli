#!/usr/bin/env python3

import click

from scripts.fetch_prots.command import fetch_prots
from scripts.downloader.command import downloader
from appindels.bulk_query import bulk_query
from appindels.query import single_query

@click.group()
def gtools():
    pass

@click.group()
def appindels():
    pass


gtools.add_command(fetch_prots)
gtools.add_command(downloader)

gtools.add_command(bulk_query)
gtools.add_command(single_query)

def main():
    gtools()
    appindels()

if __name__ == '__main__':
    main()