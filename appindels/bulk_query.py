import csv

import click
import io
import concurrent.futures
import json
from os import mkdir, path, listdir
from appindels.query import start_query, await_query, fetch_results, login, count_csis
from itertools import repeat

@click.command()
@click.argument('input_dir', type=str)
@click.argument('output_dir', type=str)
@click.option('--username', type=str, prompt=True, required=True)
@click.option('--outfile', '-o', required=False)
@click.password_option(confirmation_prompt=False)
def bulk_query(
    input_dir: str,
    output_dir: str,
    username: str,
    password: str,
    outfile: str | None = None
):
    genomes = listdir(input_dir)

    if not path.isdir(output_dir):
        mkdir(output_dir)

    session = login(username, password)
    result = [['File Name', 'Identification(s)', 'Number of CSIs', 'Raw Results']]
    try:
        # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        with click.progressbar(genomes, label='In Progress', show_pos=True) as progress_bar:
            print("woot woot")
            for genome in progress_bar:
                run_singular(genome, input_dir, output_dir, session, result)
                    # executor.submit(run_singular, genome, input_dir, output_dir, session, result)
                    # task = executor.submit(run_singular, genome, input_dir, output_dir, session, result)
                    # def cb():
                    #     progress_bar.update(1)
                    #     print("done 1")
                    # task.add_done_callback(cb)
                # executor.shutdown(wait=True)

        print('done')
    # except Exception:
    #     click.secho('Error occurred. Please check your input files.', fg='red')
    finally:
        if outfile is None or len(outfile) < 2:
            outfile = f"Results {input_dir}.csv"
        # todo: add appending to existing results
        with open(path.join(output_dir, outfile), 'w') as f:
            csv.writer(f).writerows(result)


def run_singular(genome, input_dir, output_dir, session, result):
    genome_path = path.join(input_dir, genome)
    query_id = start_query(
        open(genome_path, 'r'),
        'Bulk Query - CLI',
        session
    )

    await_query(query_id, session)
    results = fetch_results(query_id, session)
    # print(results)
    tree = json.loads(results['data']['tree'])
    n = count_csis(tree)

    result.append([genome, results['data']['identified'], n, json.dumps(results)])

    with open(path.join(output_dir, genome), 'w') as f:
        f.write(json.dumps(results, indent=4))