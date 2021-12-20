import csv
import re
from io import FileIO
from os import mkdir, path

import click

from scripts.common.exceptions import NotFoundError
from scripts.fetch_prots.engines.http import HttpDriver

ENGINES = {
    'http': HttpDriver
}


def parse_size(stats_file: str) -> int:
    search_key = 'total-length\t'
    stats_raw = re.sub(r'^#.*\n', '', stats_file, flags=re.MULTILINE)
    idx_start = stats_raw.find(search_key) + len(search_key)
    idx_end = stats_raw.find('\r\n', idx_start)
    if idx_start < 0:
        raise NotFoundError
    return round(int(stats_raw[idx_start:idx_end]) / 1000 ** 2, 1)


@click.command()
@click.argument('assembly_file', type=click.File('r'))
@click.argument('species_name', type=str)
@click.option('--skip-statistics', default=False, is_flag=True,
              help='Download files without writing an index file. Use with --skip-renaming to download raw files only.')
@click.option('--skip-renaming', default=False, is_flag=True,
              help='Skips the renaming step of downloaded files, only downloading and indexing them.')
@click.option('--output-dir', '-o', type=click.Path(exists=False),
              help='Override the directory to write the output files to. Defaults to species_name.')
@click.option('--start-at', type=int, default=0,
              help='The index of the assembly to start at.')
@click.option('--stop-at', type=int, default=None,
              help='The index of the assembly to stop at.')
@click.option('--engine', '-e', type=click.Choice(list(ENGINES.keys())), default='http',
              help='The engine to use to fetch the assemblies. Defaults to http.')
def fetch_prots(assembly_file: FileIO,
                species_name: str,
                skip_statistics: bool,
                skip_renaming: bool,
                output_dir: str | None,
                start_at: int,
                stop_at: int | None,
                engine: str) -> None:
    """
    Fetches the protein sequences for a given species from the NCBI.

    assembly_file: A CSV file from NCBI listing the assemblies to fetch.
    species_name: The species name to be used for all naming and the default name of the output folder.
    """
    if output_dir is None:
        output_dir = species_name

    assemblies = list(csv.DictReader(assembly_file))
    assemblies = assemblies[start_at:(stop_at if stop_at is not None else len(assemblies))]
    driver = ENGINES[engine]

    if not click.confirm(f'{len(assemblies)} genomes will be downloaded to {output_dir}. Continue?'):
        return click.secho('Aborting.', fg='red')

    if not path.isdir(output_dir):
        mkdir(output_dir)

    index = [['Species name', 'Strain', 'Accession no', 'GC Content (%)', 'Genome Length (mb)']]
    with click.progressbar(assemblies, label='In Progress', show_pos=True) as assemblies_bar:
        for species in assemblies_bar:
            if species['Strain'] is None or len(species['Strain']) < 1:
                continue
            if species['RefSeq FTP'] is None or len(species['RefSeq FTP']) < 1:
                species['RefSeq FTP'] = species['GenBank FTP']

            accession = species['RefSeq FTP'].split('/')[-1]
            try:
                sequence = driver.download_gz(
                    driver.format_url(species['RefSeq FTP'], f'{accession}_protein.faa.gz')
                )

                if not skip_statistics:
                    stats_file = driver.get_contents(
                        driver.format_url(species['RefSeq FTP'], f'{accession}_assembly_stats.txt'),
                    )
                    size = parse_size(stats_file)
                    index.append([species_name, species['Strain'], species["Assembly"], species['GC%'], size])
            except NotFoundError:
                click.secho(f'Could not find {accession} in {species["RefSeq FTP"]}', fg='red')
                continue

            name = f'{species_name} {species["Strain"]}'
            if not skip_renaming:
                sequence = re.sub(r'\[.+]\n', f'[{name}]\n', sequence)

            with open(f'{output_dir}/{name}.faa', 'w') as f:
                f.write(sequence)

    if not skip_statistics:
        with open(f'{output_dir}/index.csv', 'w') as f:
            click.secho(f'Writing index to {output_dir}/index.csv', fg='green')
            writer = csv.writer(f)
            writer.writerows(index)

    click.secho(f'Task Complete. Downloaded {len(assemblies)} genomes.', fg='green')

