import click
from os import mkdir, path
import requests

BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

@click.command()
@click.argument('accessions', type=str)
@click.option('--output-dir', '-o', type=click.Path(exists=False))
# todo: add --mode=both option
@click.option('--mode', type=click.Choice(['protein', 'nucleotide']), default='protein')
def downloader(
    accessions: str,
    output_dir: str,
    mode: str
):
    """
    accessions: A comma-separated list of accession numbers to be downloaded.
                To download from a file, use a Unix pipe.
    """
    assemblies = accessions.split(',')

    if not click.confirm(f'{len(assemblies)} genomes will be downloaded to {output_dir}. Continue?'):
        return click.secho('Aborting.', fg='red')

    if not path.isdir(output_dir):
        mkdir(output_dir)

    query = '+OR+'.join([f"{accn}[Accession]" for accn in assemblies])
    url = BASE_URL + f"esearch.fcgi?db{mode}&term={query}&usehistory=y"

    print(url)
    