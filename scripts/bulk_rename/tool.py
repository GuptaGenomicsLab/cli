import gzip
import os
import re

def bulk_rename(input_dir: str, output_dir: str, index_file: str, fmt: str = 'keep'):
    genomes = parse_index(index_file)
    failures = []
    # unzip all files in input_dir to output_dir

    for fname in os.listdir(input_dir):
        if fname.endswith('.gz'):
            with gzip.open(os.path.join(input_dir, fname), 'r') as f:
                sequence = str(f.read())
            fname = fname[:-3]
        else:
            with open(os.path.join(input_dir, fname), 'r') as f:
                sequence = f.read()

        accession = fname.split('_ASM')[0]
        name = genomes.get(accession)
        line_ending = '\r\n' if os.name == 'nt' else '\n'
        if name:
            sequence = re.sub(re.compile('\[.+\]' + line_ending), f'[{name}]{line_ending}', sequence)
        else:
            failures.append(accession)

        if fmt == 'txt':
            fname = fname.split('.')[:-1] + '.txt'
        elif fmt == 'fasta':
            fname = fname.split('.')[:-1] + '.fasta'

        with open(os.path.join(output_dir, fname), 'w') as f:
            f.write(sequence)

    print('Done.')
    if len(failures) > 0:
        print('Failed to rename:')
        print('\n'.join(failures))
        return failures
    return []


def parse_index(index_file: str) -> dict[str, str]:
    genomes = {}
    with open(index_file, 'r') as f:
        for line in f.readlines():
            name, *tail = re.split(r'[ \t]', line, maxsplit=1)
            genomes[name] = ' '.join(tail)
    print(genomes)
    return genomes


if __name__ == '__main__':
    bulk_rename(
        '/home/david/Development/gupta-cli/input_dir/',
        '/home/david/Development/gupta-cli/output_dir/',
        '/home/david/Development/gupta-cli/index.txt'
    )
