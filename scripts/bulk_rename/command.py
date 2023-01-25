import click

from scripts.bulk_rename.tool import bulk_rename_tool

@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=True))
@click.argument('index_file', type=click.Path(exists=True))
def bulk_rename():
    bulk_rename_tool(input_dir, output_dir, index_file)